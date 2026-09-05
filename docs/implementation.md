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

The application will later use a managed identity to authenticate to Azure resources without relying on embedded long-lived credentials.

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

## 6. Role Assignments

### Standard User Group

`NexaFlow-Standard-Users`

Role: `Storage Blob Data Reader`

Scope: NexaFlow storage account

Purpose: Allows standard users to read test blob data without granting broad Azure management permissions.

## 7. Authentication Controls

## 8. Workload Identity

## 9. Monitoring and Audit

## 10. Implementation Notes
