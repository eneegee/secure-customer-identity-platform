# Implementation — NexaFlow

## 1. Environment

- Azure subscription: Pay-As-You-Go
- Microsoft Entra ID: Free
- Security Defaults: Enabled
- Project environment: Personal learning / simulated customer environment

## 2. Identity Model

NexaFlow's implementation separates human identities into standard-user and privileged-administrator groups. The customer-facing application will use a separate workload identity rather than a human user identity.

### Standard Users

Standard employees are members of `NexaFlow-Standard-Users`.

### Privileged Administrators

Privileged administrators are members of `NexaFlow-Privileged-Admins`.

### Workload Identity

### Workload Identity

The application uses a system-assigned managed identity to authenticate to Azure resources without relying on embedded long-lived credentials.

## 3. Test Users

### Standard User

NexaFlow Standard User

Purpose: Represents a standard employee identity.

### Privileged Administrator

NexaFlow Privileged Administrator

Purpose: Represents a privileged administrative identity.

## 4. Security Groups

### NexaFlow-Standard-Users

Contains the test standard-user identity.

### NexaFlow-Privileged-Admins

Contains the test privileged-administrator identity.

## 5. Azure Resources

### Resource Group

`rg-nexaflow-identity-demo`

Purpose: Provides a scoped container for the resources used in the NexaFlow identity-security demonstration.

### Storage Account

The storage account provides a protected Azure resource for testing identity-based authorization and workload access.

### Blob Container

`nexaflow-test-data`

Purpose: Contains non-sensitive test data used to validate authorized and unauthorized access.

### Azure Container Registry

The Azure Container Registry stores the container image used by the NexaFlow application.

The project uses the Basic SKU to keep the demonstration cost-conscious. The registry is a project resource and will be removed when it is no longer required.

### Azure Container App

`nexaflow-identity-app`

Purpose: Hosts the NexaFlow customer-facing application as a containerized workload and provides a system-assigned managed identity for Azure resource access.

## 6. Role Assignments

### Standard User Group

`NexaFlow-Standard-Users`

Role: `Storage Blob Data Reader`

Scope: NexaFlow storage account

Purpose: Allows standard users to read test blob data without granting broad Azure management permissions.

### Privileged Administrator Group

`NexaFlow-Privileged-Admins`

Role: `Storage Account Contributor`

Scope: NexaFlow storage account

Purpose: Provides management-plane access to the specific storage resource.

### Privileged Administrator Data Access

`NexaFlow-Privileged-Admins`

Role: `Storage Blob Data Reader`

Scope: NexaFlow storage account

Purpose: Provides read-only access to the demonstration blob data.

### Container App → Azure Container Registry

Principal: `nexaflow-identity-app`

Role: `AcrPull`

Scope: NexaFlow Azure Container Registry

Purpose: Allows the Container App workload to pull its container image without relying on stored registry credentials.

### Container App → Azure Storage

Principal: `nexaflow-identity-app`

Role: `Storage Blob Data Reader`

Scope: NexaFlow Storage Account

Purpose: Allows the application to read the specific blob data required by the workload without granting Azure resource-management permissions or blob write/delete permissions.

## 7. Authentication Controls

### Security Defaults

Microsoft Entra Security Defaults are enabled for the tenant and provide baseline identity protection, including MFA-related protections.

### Conditional Access

Custom Conditional Access policies are not implemented in the current environment because the project uses Microsoft Entra ID Free.

Conditional Access was identified as a customer requirement during the architecture phase. A production NexaFlow environment would require an appropriate Microsoft Entra licensing arrangement to implement customized Conditional Access policies.

### Privileged Authentication

Privileged administrator identities are separated from standard employee identities and are subject to stronger access requirements defined by the identity-security design.

## 8. Workload Identity

### System-Assigned Managed Identity

The NexaFlow Container App uses a system-assigned managed identity.

The identity is separate from human employee and administrator identities and is used for service-to-service authentication to Azure resources.

### Azure Container Registry Access

The Container App's managed identity is assigned the `AcrPull` role on the NexaFlow Azure Container Registry.

This allows the workload to pull its container image without relying on stored registry credentials.

### Azure Storage Access

The Container App's managed identity is assigned the `Storage Blob Data Reader` role on the NexaFlow Storage Account.

This allows the application to read the required blob data without granting Azure resource-management permissions or blob write/delete permissions.

### Application Authentication

The application uses the Azure Identity SDK and `DefaultAzureCredential` to obtain an identity-based Azure credential when running in Azure.

The application connects to Azure Blob Storage using its managed identity rather than a storage account key, connection string, or embedded long-lived credential.

### Application Configuration

The application receives the following non-secret configuration through environment variables:

- `STORAGE_ACCOUNT_NAME`
- `CONTAINER_NAME`
- `BLOB_NAME`

No authentication credentials are stored in these environment variables.

## 9. Monitoring and Audit

The project requires visibility into identity and access activity to support security investigation and validation.

Identity and resource activity will be reviewed through the available Azure monitoring and audit capabilities.

Detailed monitoring validation will be completed during the testing phase.

## 10. Implementation Notes

The application uses one system-assigned managed identity with resource-specific permissions.

The identity is authorized separately to pull its container image from Azure Container Registry and to read required blob data from Azure Storage.

The application does not receive broad Azure management permissions.

### Management Plane vs Data Plane

The implementation distinguishes Azure resource management permissions from access to storage data.

The privileged administrator receives `Storage Account Contributor` for management of the specific storage account and `Storage Blob Data Reader` for read-only access to blob data.

The application workload receives only `Storage Blob Data Reader` and does not receive storage-management permissions.

### Human Identity vs Workload Identity

Human identities are used for interactive access and administration, while the application uses a separate managed identity for service-to-service access.

This separation allows workload permissions to be controlled independently from human-user permissions and reduces dependence on long-lived application credentials.
