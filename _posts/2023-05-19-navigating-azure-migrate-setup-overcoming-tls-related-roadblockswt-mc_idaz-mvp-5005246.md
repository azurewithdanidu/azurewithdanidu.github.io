---
title: "Navigating Azure Migrate Setup: Overcoming TLS-related Roadblocks."
date: 2023-05-19
categories: 
  - "azure"
  - "azure-migrate"
tags: 
  - "azuresiterecovery"
  - "azurevm"
---

Howdy Folks

As an Azure consultant, I often come across diverse challenges in setting up systems and ensuring smooth migrations for my clients. Recently, while working on a customer project that involved migrating servers using Azure Migrate, we encountered a series of puzzling errors. Today, I’d like to share how we managed to resolve the issue and the key learnings from this experience.

Azure Migrate, a service by Microsoft, allows organizations to carry out large-scale migration of servers to the cloud. A critical part of this process is setting up the Process Server, an Azure Migrate component that handles replication management and data transport.

In our case, configuring the Process Server was far from a walk in the park. We were greeted with a barrage of error messages, leading us to suspect that our proxy settings were causing the issue. However, after extensive troubleshooting, we discovered the real culprit was outdated Transport Layer Security (TLS) protocols, namely TLS 1.0 and 1.1.

I was able to find below error in system log too.

[![](images/image-1.png)](https://hungryboysl.wordpress.com/wp-content/uploads/2023/05/image-1.png)

### The Issue with Outdated TLS Protocols

TLS protocols are vital for secure communication between web servers and clients. However, TLS 1.0 and 1.1, being older versions, lack the robust security features of newer protocols, especially TLS 1.2 and 1.3. Many systems and applications, including Azure Migrate, have phased out support for TLS 1.0 and 1.1 due to their inherent vulnerabilities.

### The Solution: Enabling Strong Cryptography and Defaulting to Modern TLS

Our solution involved modifying specific registry keys to ensure .NET Framework defaulted to using stronger cryptography and more secure TLS protocols. We enabled SystemDefaultTlsVersions and SchUseStrongCrypto and set the system to default to TLS 1.2 for both the server and client.

Here are the registry modifications we implemented:

```
If (-Not (Test-Path 'HKLM:\SOFTWARE\WOW6432Node\Microsoft\.NETFramework\v4.0.30319')) {
    New-Item 'HKLM:\SOFTWARE\WOW6432Node\Microsoft\.NETFramework\v4.0.30319' -Force | Out-Null
}
New-ItemProperty -Path 'HKLM:\SOFTWARE\WOW6432Node\Microsoft\.NETFramework\v4.0.30319' -Name 'SystemDefaultTlsVersions' -Value '1' -PropertyType 'DWord' -Force | Out-Null
New-ItemProperty -Path 'HKLM:\SOFTWARE\WOW6432Node\Microsoft\.NETFramework\v4.0.30319' -Name 'SchUseStrongCrypto' -Value '1' -PropertyType 'DWord' -Force | Out-Null

 

If (-Not (Test-Path 'HKLM:\SOFTWARE\Microsoft\.NETFramework\v4.0.30319')) {
    New-Item 'HKLM:\SOFTWARE\Microsoft\.NETFramework\v4.0.30319' -Force | Out-Null
}
New-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\.NETFramework\v4.0.30319' -Name 'SystemDefaultTlsVersions' -Value '1' -PropertyType 'DWord' -Force | Out-Null
New-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\.NETFramework\v4.0.30319' -Name 'SchUseStrongCrypto' -Value '1' -PropertyType 'DWord' -Force | Out-Null

 

If (-Not (Test-Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.2\Server')) {
    New-Item 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.2\Server' -Force | Out-Null
}
New-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.2\Server' -Name 'Enabled' -Value '1' -PropertyType 'DWord' -Force | Out-Null
New-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.2\Server' -Name 'DisabledByDefault' -Value '0' -PropertyType 'DWord' -Force | Out-Null

 

If (-Not (Test-Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.2\Client')) {
    New-Item 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.2\Client' -Force | Out-Null
}
New-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.2\Client' -Name 'Enabled' -Value '1' -PropertyType 'DWord' -Force | Out-Null
New-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.2\Client' -Name 'DisabledByDefault' -Value '0' -PropertyType 'DWord' -Force | Out-Null

I was able to find the registry details from below
https://www.alitajran.com/a-fatal-error-occurred-while-creating-a-tls-client-credential/
```

### Conclusion

Solving this TLS issue was an enlightening experience and a reminder that even in an age where cloud-based systems like Azure are designed to ease our IT burdens, challenges can arise from unexpected corners. However, by being methodical in our approach and understanding the underlying technologies, we can navigate these hurdles. The journey to the cloud may be complicated, but with the right knowledge and tools, it's a journey we can successfully undertake.

If you're an Azure consultant or an IT professional dealing with similar challenges, I hope that sharing our experience can help shed light on your path. And remember, when facing such issues, always consider checking the security protocols - it could save you a considerable amount of troubleshooting time.

For further reading, please refer to the official Microsoft documentation:

- [Understanding Azure Migrate](https://docs.microsoft.com/en-us/azure/migrate/migrate-services-overview)

- [Azure Migrate: Server Migration](https://docs.microsoft.com/en-us/azure/migrate/tutorial-migrate-physical-virtual-machines)

- [Transport Layer Security (TLS) registry settings](https://docs.microsoft.com/en-us/windows-server/security/tls/tls-registry-settings)

- [.NET Framework strong cryptography registry keys](https://docs.microsoft.com/en-us/dotnet/framework/network-programming/tls)

Happy migrating!
