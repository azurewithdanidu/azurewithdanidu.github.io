---
title: "Running And Securing FTP Service in Azure"
date: 2025-10-14
categories: 
  - "azure"
  - "azure-infrastructure"
  - "ftp"
  - "security"
  - 'storage'
tags: 
  - "bicep"
  - "compute"
  - "infrastructure"
  - "networking"
  - "security"
  - "storage"
---

Howdy Folks,

In this post, we will explore how to set up and secure an FTP service in Microsoft Azure. FTP (File Transfer Protocol) is a standard network protocol used for transferring files between a client and server. While FTP is widely used, it is important to implement security measures to protect data during transfer. Mostly we talk about hosting app services, databases, and other cloud-native solutions, but sometimes you need to run legacy services like FTP. In this guide, we will cover the necessary steps to deploy an FTP service in Azure using Azure Blob Storage for file storage, and we will implement security best practices to ensure safe file transfers.

Let's get started!

First lets talk about few possible architectures for running FTP in Azure using Storage Accounts: 
Architectures depends on your requirements and your current environment and budget. Here are a few common architectures:

1. **SFTP Enabled Storage Account with Storage Account Firewall**: 
   - Use Azure Blob Storage with SFTP enabled for secure file transfers.
   - Configure the Storage Account firewall to restrict access to specific IP addresses or virtual networks.
   - This is the simplest and most cost-effective solution for secure file transfers.

![alt text](./images/image.png)


2. **SFTP Enabled Storage Account with Azure Firewall configuration**:
   - Use Azure Blob Storage with SFTP enabled for secure file transfers.
   - Configure Azure Firewall to restrict access to the Storage Account based on IP addresses or virtual networks.
   - This solution provides an additional layer of security by leveraging Azure Firewall capabilities.
   - This will be a bit more expensive than the first option.
   - Also this will provide more visibility and control over the traffic.

![alt text](./images/image-1.png)