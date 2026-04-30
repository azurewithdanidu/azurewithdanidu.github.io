---
title: "Centralizing Private DNS Zone Permission Management in Azure Landing Zones"
date: 2026-04-30 08:00:00 +1000
categories: [Azure, Networking]
tags: [private-dns, private-endpoints, rbac, bicep, landing-zones, networking, azure-policy]
description: "A real-world pattern for granting developers just enough permission to manage their own private endpoint DNS records in a centralized DNS architecture — without giving them the keys to the kingdom."
author: Danidu Weerasinghe
toc: true
comments: true
pin: false
mermaid: false
math: falseg
---

Howdy Folks,

This one comes straight from the field. A real problem I ran into with a customer, and I wanted to share how I handled it — because I suspect quite a few of you are running into the same thing. It may not be the only way to solve it, but it is a way that worked well in practice.

Let's dive in!


## The Setup

The customer had a well-structured **Azure Landing Zone** architecture with centralized networking. Their DNS setup looked like this:

```
Landing Zones (Dev, Test, Prod)
        |
        | DNS queries via custom DNS server
        v
[Azure Private DNS Resolver] <-- Hub VNet
        |
        v
[Centralized Private DNS Zones] <-- Managed by Platform/Network Team
  e.g., privatelink.blob.core.windows.net
        privatelink.vaultcore.azure.net
        privatelink.database.windows.net
        ...
```

The rules were clear:

- **Developers are NOT allowed to create their own Private DNS Zones** in their landing zone subscriptions.
- **All VNets point to the Private DNS Resolver** as their custom DNS server.
- An **Azure Policy** is in place to automatically register DNS A-records in the central zones whenever a Private Endpoint is deployed.

This is a solid, enterprise-grade setup. The platform team controls the DNS namespace, and Azure Policy handles auto-registration. What could go wrong?


## The Problem

Three things, actually.

### 1. Developers couldn't manually create DNS records when needed

Azure Policy takes care of DNS registration most of the time — but sometimes developers need to create the Private Endpoint manually and the policy assignment hasn't kicked in yet, or there's a timing issue, or they're troubleshooting. When they navigated to the central Private DNS Zone to check or add a record, they got a flat-out permission denied. They couldn't even **see** the zone details, let alone add a record.

### 2. Deleting Private Endpoints was throwing errors

When a developer deleted a Private Endpoint, the deletion process also attempts to clean up the associated DNS A-record in the linked Private DNS Zone. Because they had no permission on the central DNS zone, that cleanup step **failed** — leaving orphaned DNS records behind, and causing confusion for the developer who just wanted to delete their resource cleanly.

### 3. The platform team was becoming a bottleneck

Every DNS-related issue meant raising a ticket and waiting for the central team to intervene. Not ideal! Developers were frustrated, and the platform team was spending time on routine DNS record management instead of higher-value work.


## The Goals

Before jumping to a solution, I needed to be clear on what I was trying to achieve:

1. **Enable developer self-service** — they should be able to create and delete Private Endpoint DNS records without needing the platform team.
2. **Protect the DNS zone** — developers should NOT be able to see or modify records belonging to other teams or services.
3. **Least privilege** — give them exactly what they need, nothing more.

The key insight here? I needed developers to be able to **write and delete their own A-records**, but I did **not** want them to be able to **list all records in the zone** — which would give them visibility into DNS records for other teams' Private Endpoints.


## The Solution: A Custom RBAC Role

Azure's built-in roles weren't quite right here. `DNS Zone Contributor` gives too much access — it allows listing all records and modifying zone settings. There was no built-in role that fit this specific "write your own records, but don't browse the zone" use case.

So the solution was a **custom RBAC role** assigned to developers (or their workload identity/managed identity) at the **Private DNS Zone scope** in the central subscription.

Here are the permissions:

```
Microsoft.Network/privateDnsZones/read
Microsoft.Network/privateDnsZones/A/read
Microsoft.Network/privateDnsZones/A/write
Microsoft.Network/privateDnsZones/A/delete
Microsoft.Network/privateDnsZones/join/action
Microsoft.Network/privateEndpoints/privateDnsZoneGroups/write
Microsoft.Network/privateEndpoints/privateDnsZoneGroups/read
Microsoft.Resources/deployments/*
Microsoft.Resources/subscriptions/resourceGroups/read
```

## Key Permission Breakdown

Let me walk through the important ones:

### `Microsoft.Network/privateDnsZones/read`

This allows developers to **see the Private DNS Zone resource** (the zone itself), but it does **not** grant visibility into the individual DNS records inside it. So they can confirm the zone exists and link to it, but they can't browse everyone else's A-records. This is the critical nuance that makes this approach work.

> This is the permission that makes the magic happen — zone visibility without record visibility.
{: .prompt-tip }

### `Microsoft.Network/privateDnsZones/A/write` and `/A/delete`

These two permissions allow the Private Endpoint creation and deletion processes to **write and remove A-records** in the zone. When a developer creates a Private Endpoint with a DNS Zone Group configured, Azure needs to create the A-record. When they delete the PE, Azure needs to remove it. Without these, both operations fail.

> Since developers cannot list all records, they can only interact with records through their own Private Endpoint management — they can't go and arbitrarily delete another team's records.
{: .prompt-info }

### `Microsoft.Network/privateDnsZones/join/action`

Required to **link the Private DNS Zone to a Private Endpoint DNS Zone Group**. Without this, the PE creation wizard will fail when trying to configure the DNS integration.

### `Microsoft.Network/privateEndpoints/privateDnsZoneGroups/write` and `/read`

These allow developers to **configure and view the DNS Zone Group** on a Private Endpoint — which is the linkage between the PE and the central DNS zone.

### `Microsoft.Resources/deployments/*` and `Microsoft.Resources/subscriptions/resourceGroups/read`

These are supporting permissions needed for ARM deployments to work correctly when creating resources that span resource groups (i.e., the PE in the landing zone subscription linking to the DNS zone in the hub subscription).


## Bicep: Deploying the Custom Role Definition

Here's the Bicep to deploy this custom role at the subscription scope. You would deploy this targeting the **hub/connectivity subscription** where the Private DNS Zones live.

```bicep
targetScope = 'subscription'

@description('A unique GUID for the custom role definition. Generate once and store.')
param roleDefinitionId string = newGuid()

resource privateDnsContributorRole 'Microsoft.Authorization/roleDefinitions@2022-04-01' = {
  name: roleDefinitionId
  properties: {
    roleName: 'Private Endpoint DNS Contributor'
    description: 'Allows workloads to create and delete their own Private Endpoint A-records in centralized Private DNS Zones, without visibility into other records.'
    type: 'CustomRole'
    assignableScopes: [
      subscription().id
    ]
    permissions: [
      {
        actions: [
          'Microsoft.Network/privateDnsZones/read'
          'Microsoft.Network/privateDnsZones/A/read'
          'Microsoft.Network/privateDnsZones/A/write'
          'Microsoft.Network/privateDnsZones/A/delete'
          'Microsoft.Network/privateDnsZones/join/action'
          'Microsoft.Network/privateEndpoints/privateDnsZoneGroups/write'
          'Microsoft.Network/privateEndpoints/privateDnsZoneGroups/read'
          'Microsoft.Resources/deployments/*'
          'Microsoft.Resources/subscriptions/resourceGroups/read'
        ]
        notActions: []
        dataActions: []
        notDataActions: []
      }
    ]
  }
}

output roleDefinitionResourceId string = privateDnsContributorRole.id
```

> **Important**: The `roleDefinitionId` parameter uses `newGuid()` as a default. For production use, generate a stable GUID once and hardcode it — otherwise each deployment will create a new role definition. Use `az role definition list --name 'Private Endpoint DNS Contributor'` to check if the role already exists before deploying.
{: .prompt-warning }

You would then assign this role to your developers or their managed identities at the **scope of each relevant Private DNS Zone** in the hub subscription.

```bicep
resource roleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(privateDnsZone.id, principalId, privateDnsContributorRole.id)
  scope: privateDnsZone
  properties: {
    roleDefinitionId: privateDnsContributorRole.id
    principalId: '<developer-group-or-managed-identity-object-id>'
    principalType: 'Group' // or 'ServicePrincipal' for managed identities
  }
}
```


## How This Looks in Practice

Once the custom role is assigned, here's what changes for developers:

| Action | Before | After |
|--------|--------|-------|
| View Private DNS Zone in portal | ❌ Permission denied | ✅ Can see the zone resource |
| Browse all DNS records in zone | ❌ Not possible | ❌ Still not possible (by design) |
| Create Private Endpoint with DNS Zone Group | ❌ Fails on DNS record creation | ✅ Works end-to-end |
| Delete Private Endpoint | ❌ Fails on DNS record cleanup | ✅ Cleans up cleanly |
| Delete another team's DNS records | ❌ Not possible | ❌ Still not possible (by design) |

The developers get exactly what they need. The platform team stops being the DNS bottleneck. And the central DNS zone remains protected. Win-win-win.


## Things to Consider

- **Assign the role at the DNS Zone level, not the subscription level.** This ensures developers only have this access to the specific zones they need, not everything in the hub subscription.
- **If you're using Azure Policy for auto-registration**, this role is still useful as a safety net for edge cases where policy timing causes issues or when developers work outside of IaC pipelines.
- **Consider using Managed Identities** for CI/CD pipelines and workload identities rather than assigning this directly to individual users — it's more scalable and easier to audit.


## Useful References

- [Azure Private Endpoint DNS integration — Microsoft Learn](https://learn.microsoft.com/en-us/azure/private-link/private-endpoint-dns-integration)
- [Azure Private DNS zone overview — Microsoft Learn](https://learn.microsoft.com/en-us/azure/dns/private-dns-privatednszone)
- [Azure custom roles — Microsoft Learn](https://learn.microsoft.com/en-us/azure/role-based-access-control/custom-roles)
- [Private Endpoint DNS zone values — Microsoft Learn](https://learn.microsoft.com/en-us/azure/private-link/private-endpoint-dns)


Hope this helps someone who's been hitting the same wall! It's a fairly common pattern in enterprise Landing Zone deployments, and the solution is elegant once you find that sweet spot between `privateDnsZones/read` (zone visibility) and the absence of `privateDnsZones/*/read` (record listing).

Feel free to reach out if you have any questions or if you're hitting a variation of this problem. Until next time...!

