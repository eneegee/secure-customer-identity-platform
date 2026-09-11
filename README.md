# Secure Customer Identity Platform — NexaFlow

A cost-conscious simulated customer solution demonstrating secure identity, least-privilege access, workload authentication, privileged-access separation, and security validation on Microsoft Azure.

---

## Project Overview

NexaFlow is a fictional growing B2B SaaS company preparing to launch a customer-facing application.

The organization needed a more secure identity and access model because its existing approach presented several risks:

- Excessive permissions.
- Insufficient separation between standard and privileged users.
- Inconsistent multifactor authentication.
- Application credential exposure risk.
- Limited identity visibility and auditability.
- Lack of a documented access model.

This project was designed as a simulated customer engagement rather than a standalone Azure lab.

The solution focuses on designing, implementing, testing, and documenting a secure Azure identity architecture while balancing security, operational simplicity, licensing, and cost.

---

## Business Requirements

The solution needed to provide:

- Strong authentication for human identities.
- Separation between standard and privileged users.
- Least-privilege authorization.
- Secure authentication for application workloads.
- Removal of embedded long-lived application credentials.
- Controlled access to Azure resources.
- Auditability of authentication and administrative activity.
- A design that can scale as NexaFlow grows.
- Cost-conscious implementation suitable for the current environment.

---

## Identity Model

The solution separates identities into three categories.

### Standard Users

Standard employees are represented through:

`NexaFlow-Standard-Users`

Standard users receive only the access required for their normal responsibilities.

They are not granted Azure management-plane permissions.

### Privileged Administrators

Privileged users are separated into:

`NexaFlow-Privileged-Admins`

Their administrative permissions are explicitly scoped to the resources they need to manage.

### Workload Identity

The customer-facing application uses a **system-assigned managed identity**.

This allows the application to authenticate to Azure services without storing long-lived Azure credentials in the application.

---

## Architecture

```text
                         Microsoft Entra ID
                                │
                ┌───────────────┴───────────────┐
                │                               │
        Standard Users                 Privileged Admins
                │                               │
       Security Defaults                Security Defaults
             & MFA                           & MFA
                │                               │
                │                      Scoped Azure RBAC
                │                               │
                └──────────────┬────────────────┘
                               │
                              Azure
                               │
              ┌────────────────┴────────────────┐
              │                                 │
       Azure Container App                Azure Storage
              │                                 │
     System-Assigned                     Private Blob
      Managed Identity                    Container
              │                                 │
              ├── AcrPull → ACR                 │
              │                                 │
              └── Storage Blob Data Reader ─────┘
```

---

## Azure Resources

The implementation uses:

- Microsoft Entra ID
- Azure Resource Groups
- Azure Storage
- Azure Blob Storage
- Azure Container Registry
- Azure Container Apps
- Azure RBAC
- Managed Identities
- Microsoft Entra Security Defaults
- Microsoft Authenticator
- Microsoft Entra Sign-in Logs
- Azure Activity Log
- Azure Cloud Shell

Primary resource group:

`rg-nexaflow-identity-demo`

---

## Application

A small Python/Flask application was containerized and deployed to Azure Container Apps.

The application exposes:

```text
/
```

Application landing endpoint.

```text
/health
```

Application health endpoint.

```text
/data
```

Protected application functionality that retrieves test data from Azure Blob Storage.

The application uses the Azure Identity SDK to obtain Azure credentials through its managed identity.

No storage account key or connection string is embedded in the application.

---

## Workload Identity Security

The Container App uses a **system-assigned managed identity**.

The identity receives separate resource-specific permissions.

### Azure Container Registry

Role:

`AcrPull`

Purpose:

Allows the application to retrieve its container image without storing registry credentials.

### Azure Storage

Role:

`Storage Blob Data Reader`

Purpose:

Allows the application to read the blob data required by the workload.

The identity does not receive blob write or delete permissions.

---

## Human Identity Security

### Standard User

The standard user:

- Authenticates through Microsoft Entra ID.
- Is protected by MFA through Security Defaults.
- Does not receive Azure management-plane access.
- Cannot access the NexaFlow resource environment as an administrator.

### Privileged Administrator

The privileged administrator:

- Authenticates through Microsoft Entra ID.
- Is protected by MFA.
- Receives scoped storage-management permissions.
- Receives read-only blob data access through Microsoft Entra RBAC.

Assigned roles include:

```text
Storage Account Contributor
Storage Blob Data Reader
```

The assignments are scoped to the NexaFlow storage account rather than the wider project resource group.

---

## Management Plane vs Data Plane

An important part of the project was separating Azure resource-management permissions from access to the data stored inside those resources.

### Management Plane

Controls operations such as:

- Managing Azure resources.
- Updating storage configuration.
- Managing access control.
- Configuring resource settings.

### Data Plane

Controls operations such as:

- Reading blobs.
- Uploading blobs.
- Modifying blobs.
- Deleting blobs.

This distinction was explicitly tested during the project.

---

## Security Validation

The implementation was tested rather than assumed to be secure.

### Managed Identity Testing

The workload identity was tested for:

| Test | Result |
|---|---|
| Read required blob data | PASS |
| Upload unauthorized blob | DENIED — PASS |
| Delete protected blob | DENIED — PASS |

The application could perform its required read operation while write and delete operations were blocked.

---

## MFA Validation

Both human test identities were required to authenticate using Microsoft Authenticator.

Microsoft Entra sign-in logs confirmed:

- Successful authentication.
- Multifactor authentication requirement.
- MFA satisfaction.
- Security Defaults involvement.

Custom Conditional Access policies were not implemented because the current environment uses Microsoft Entra ID Free.

Security Defaults was therefore used as the baseline MFA control.

---

## Standard User Authorization Testing

The `NexaFlow Standard User` successfully authenticated to Azure but could not access the NexaFlow Azure management environment.

Direct access produced:

```text
You do not have access
```

This demonstrated that successful authentication does not automatically provide Azure resource-management authorization.

---

## Privileged Access Testing

The privileged administrator was tested separately.

Using Microsoft Entra authentication:

| Operation | Result |
|---|---|
| Authenticate with MFA | PASS |
| Access authorized storage resource | PASS |
| Read blob data | PASS |
| Write blob data | DENIED — PASS |
| Delete blob data | DENIED — PASS |

Azure CLI testing used:

```text
--auth-mode login
```

to ensure that the tests were performed using the signed-in Microsoft Entra identity rather than a storage account key.

---

## Security Finding — Shared Key Authorization

During testing, an unexpected behavior was discovered.

A blob upload succeeded through the Azure portal even though the privileged administrator had only read-only blob data permissions.

Further investigation identified an alternate **Shared Key authorization path**.

The privileged administrator's storage-management permissions could interact with storage account keys, creating an authorization path that did not reflect the intended Microsoft Entra read-only data permissions.

This was an important finding because the assigned RBAC roles appeared correct while another authentication mechanism changed the effective access behavior.

---

## Remediation

The following changes were implemented:

1. Privileged RBAC assignments were reduced from resource-group scope to the specific storage account.

2. Shared Key authorization was disabled.

3. Microsoft Entra authentication became the intended blob-data authorization path.

4. Blob read, write, and delete tests were repeated.

After remediation:

```text
Read   → Allowed
Write  → Denied
Delete → Denied
```

The expected least-privilege model was successfully validated.

---

## Residual Risk

The privileged administrator retains storage-account management permissions.

An identity with sufficient management authority may be capable of changing security-related storage configuration.

In a stricter production environment, this risk could be reduced through controls such as:

- Custom Azure RBAC roles.
- Separation of duties.
- Azure Policy.
- Microsoft Entra Privileged Identity Management.
- Conditional Access.
- Just-in-time privileged access.

These controls were outside the scope of the current implementation.

---

## Logging and Auditability

The project also validated whether security activity could be observed and attributed.

### Microsoft Entra Sign-in Logs

Sign-in activity for both:

- `NexaFlow Standard User`
- `NexaFlow Privileged Administrator`

was visible in Microsoft Entra.

The logs showed:

- Successful sign-ins.
- MFA requirement.
- Authentication information.
- Security Defaults involvement.

### Azure Activity Log

Management-plane operations were also recorded.

Validated events included:

```text
Update Storage Account
Create role assignment
List Storage Account Keys
```

The events contained:

- Operation name.
- Status.
- Initiating identity.
- Resource.
- Resource group.
- Timestamp.

This demonstrated administrative accountability and auditability.

---

## Key Security Controls

The project demonstrates:

- Microsoft Entra identity management.
- MFA through Security Defaults.
- Separation of standard and privileged identities.
- Azure RBAC.
- Least privilege.
- Resource-level permission scoping.
- Managed identities.
- Credential-less workload authentication.
- Management-plane/data-plane separation.
- Shared Key hardening.
- Authentication-path analysis.
- Security testing.
- Remediation and retesting.
- Sign-in monitoring.
- Administrative audit logging.

---

## Security Testing Results

| Validation | Result |
|---|---|
| Managed identity authentication | PASS |
| Authorized workload blob read | PASS |
| Unauthorized workload write denied | PASS |
| Unauthorized workload delete denied | PASS |
| Standard-user MFA | PASS |
| Standard-user management access denied | PASS |
| Privileged-admin MFA | PASS |
| Privileged scoped management access | PASS |
| Privileged Entra blob read | PASS |
| Privileged Entra blob write denied | PASS |
| Privileged Entra blob delete denied | PASS |
| Shared Key security issue identified | IDENTIFIED |
| Shared Key issue remediated | PASS |
| RBAC scope hardened | PASS |
| Human sign-in logging | PASS |
| Azure administrative auditability | PASS |

---

## Project Documentation

Detailed project documentation is available in the `docs/` directory:

- [Customer Discovery](docs/customer-discovery.md)
- [Threat Model](docs/threat-model.md)
- [Architecture Decision](docs/architecture-decision.md)
- [Implementation](docs/implementation.md)
- [Security Testing](docs/testing.md)

---

## Repository Structure

```text
secure-customer-identity-platform/
│
├── README.md
├── .gitignore
│
├── docs/
│   ├── customer-discovery.md
│   ├── threat-model.md
│   ├── architecture-decision.md
│   ├── implementation.md
│   └── testing.md
│
├── app/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
│
└── screenshots/
    └── project evidence
```

---

## Selected Evidence

Evidence captured during implementation includes:

- Running Azure Container App.
- System-assigned managed identity.
- Azure Container Registry `AcrPull` assignment.
- Azure Storage RBAC configuration.
- Application health validation.
- Managed identity access to Azure Storage.
- Microsoft Authenticator requirement.
- Standard-user access denial.
- Privileged-user write denial.
- Privileged-user delete denial.

See the [`screenshots/`](screenshots/) directory for project evidence.

---

## Architecture Decisions

The implementation intentionally balanced security, cost, and project scope.

The selected architecture used:

- Microsoft Entra ID.
- Security Defaults instead of licensed Conditional Access.
- Azure RBAC.
- System-assigned managed identity.
- Resource-specific permissions.
- Identity-based Azure Storage authentication.
- Azure-native logging and auditing.

Enterprise IAM platforms, enterprise PAM products, multi-region architecture, production disaster recovery, full SIEM/SOC implementation, and third-party identity providers were intentionally excluded from the project scope.

---

## Key Lessons

This project reinforced several important cloud-security principles.

### Authentication is not authorization

A user may authenticate successfully while still being denied access to Azure resources.

### Management access is different from data access

Azure resource-management roles do not automatically represent the same permissions over the underlying data.

### Assigned RBAC roles are not the entire access story

Alternate authentication mechanisms such as Shared Key can affect effective authorization.

### Least privilege must be validated

A role assignment appearing correct in the portal does not prove that the effective access boundary behaves as intended.

### Security testing can change architecture

Testing uncovered an alternate authorization path, which led to RBAC scope correction and Shared Key hardening.

### Auditability matters

Security controls are stronger when authentication and administrative actions can be attributed to specific identities.

---

## Skills Demonstrated

This project provided hands-on experience with:

- Azure identity architecture.
- Microsoft Entra ID.
- Azure RBAC.
- MFA.
- Privileged-access design.
- Managed identities.
- Azure Storage security.
- Azure Container Apps.
- Azure Container Registry.
- Python application deployment.
- Containerization.
- Authentication and authorization testing.
- Azure CLI.
- Azure Cloud Shell.
- Security troubleshooting.
- Threat modeling.
- Architecture decision-making.
- Logging and audit analysis.
- Security remediation.
- Technical documentation.

---

## Project Status

**Complete**

The implementation and defined security validation have been completed.

The project demonstrates the lifecycle of a simulated customer security engagement:

```text
Customer Discovery
        ↓
Threat Modeling
        ↓
Architecture Decision
        ↓
Implementation
        ↓
Security Testing
        ↓
Unexpected Finding
        ↓
Root-Cause Investigation
        ↓
Remediation
        ↓
Retesting
        ↓
Audit Validation
        ↓
Documented Security Outcome
```

---

## Disclaimer

This project was completed in a personal Azure learning environment using a fictional customer scenario.

It demonstrates hands-on implementation and security testing experience and should not be interpreted as production deployment experience.
