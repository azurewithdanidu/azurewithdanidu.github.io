---
title: "You need to start using bicep parameter files now.!"
date: 2023-08-06
categories: 
  - "azure"
tags: 
  - "bicep"
  - "devops"
---

In Azure Bicep, parameters play a crucial role in enabling flexibility and reusability within templates. These parameters allow dynamic values to be passed into the template, and they can include default values and input value constraints.

Instead of directly including parameters as inline values within your deployment script, you have the option to employ a Bicep parameters file, saved with the .bicepparam file extension, or a JSON parameters file. These files store the parameter values separately.

There are few things to note though. It's not like typical Json parameter files or yaml variable files.

A single Bicep file can have multiple Bicep parameters files associated with it. However, each Bicep parameters file is intended for one particular Bicep file. This relationship is established using the using statement within the Bicep parameters file.

[![](images/image.png)](https://hungryboysl.wordpress.com/wp-content/uploads/2023/08/image.png)

It's important to highlight that the parameters file stores parameter values as plain text. However, for security considerations, it's advisable not to employ this method for storing sensitive information, such as passwords. When dealing with parameters that contain confidential data, like passwords, it's recommended to store them in a secure key vault. Rather than including the sensitive value directly in your parameters file, you can utilize the [getSecret](https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/bicep-functions-resource#getsecret) function to fetch and retrieve it securely.

## Parameter Data Types

You can pretty much define string, integer, boolean, array, and object types as parameters using this new file format.

### Object and Array

[![](images/image-1.png)](https://hungryboysl.wordpress.com/wp-content/uploads/2023/08/image-1.png)

### Strings and Ints

[![](images/image-2.png)](https://hungryboysl.wordpress.com/wp-content/uploads/2023/08/image-2.png)

## How to Generate parameter files using VS codes

As you may already know its easier to generate json parameter files using VS Code to generate biceparm files we have to do pretty much the same thing.

Follow the below steps to generate a bicepparm parameter file.

**Right Click on the bicep file** and Select Generate Parameter file

[![](images/image-3.png)](https://hungryboysl.wordpress.com/wp-content/uploads/2023/08/image-3.png)

From the drop down select bicepparam.

[![](images/image-4.png)](https://hungryboysl.wordpress.com/wp-content/uploads/2023/08/image-4.png)

There is no easy way to covert your existing json to bicepparam files unfortunately.  
Hope you gonna enjoy using bicepparam files :)

Untill next time.........................
