# Security Testing — NexaFlow

## 1. Purpose

This document records the security validation performed for the NexaFlow Secure Customer Identity Platform.

The purpose of the testing was to verify that the implemented identity and access controls behave as intended rather than relying only on configuration settings.

The validation focused on:

- Workload identity authentication.
- Least-privilege Azure Storage access.
- Denial of unauthorized workload operations.
- Multifactor authentication for human identities.
- Separation between standard-user and privileged access.
- Azure management-plane authorization.
- Microsoft Entra data-plane authorization.
- Identification of alternate authorization paths.
- Security remediation.
- Sign-in logging and management-plane auditability.

---

## 2. Test Environment

### Azure Environment

- Azure subscription: Pay-As-You-Go
- Microsoft Entra ID: Free
- Security Defaults: Enabled
- Project environment: Personal learning / simulated customer environment
- Resource group: `rg-nexaflow-identity-demo`
- Storage account: `nexaflowidentity20260905`
- Blob container: `nexaflow-test-data`
- Test blob: `nexaflow-test.txt`
- Container App: `nexaflow-identity-app`

### Human Identities

- `NexaFlow Standard User`
- `NexaFlow Privileged Administrator`

### Security Groups

- `NexaFlow-Standard-Users`
- `NexaFlow-Privileged-Admins`

### Workload Identity

The application uses a system-assigned managed identity.

The managed identity has:

- `AcrPull` on the NexaFlow Azure Container Registry.
- `Storage Blob Data Reader` on the NexaFlow storage account.

### Privileged Administrator Permissions

The `NexaFlow-Privileged-Admins` group has:

- `Storage Account Contributor`
- `Storage Blob Data Reader`

These permissions are scoped to the NexaFlow storage account.

---

## 3. Test A — Managed Identity Authorized Blob Read

### Objective

Verify that the deployed Container App can authenticate to Azure Storage using its system-assigned managed identity and read the blob data required by the application.

### Test

The deployed application `/data` endpoint was accessed.

The application attempted to retrieve:

`nexaflow-test.txt`

from:

`nexaflow-test-data`

using Azure identity-based authentication.

### Expected Result

The application should successfully authenticate to Azure and read the test blob without using a storage account key or connection string.

### Actual Result

The application successfully retrieved the authorized blob data.

### Result

**PASS**

### Security Significance

This demonstrates that the application workload can access the Azure Storage data it requires through its managed identity.

The application does not require embedded long-lived storage credentials for the demonstrated access path.

---

## 4. Test B — Managed Identity Unauthorized Blob Write

### Objective

Verify that the Container App managed identity cannot write blob data beyond its assigned permissions.

### Test

A blob upload operation was executed from the Azure Container App console using the application's managed identity.

The application attempted to create:

`nexaflow-write-test.txt`

### Expected Result

The operation should be denied because the workload identity has `Storage Blob Data Reader`, which does not grant blob write permissions.

### Actual Result

Azure returned:

```text
ErrorCode:AuthorizationPermissionMismatch
Content: <?xml version="1.0" encoding="utf-8"?><Error><Code>AuthorizationPermissionMismatch</Code><Message>This request is not authorized to perform this operation using this permission.
```

### Result

**PASS**

### Security Significance

The workload identity authenticated successfully but was not authorized to modify blob data.

This demonstrates enforcement of least privilege for the application's Azure Storage data-plane permissions.

---

## 5. Test C — Managed Identity Unauthorized Blob Delete

### Objective

Verify that the Container App managed identity cannot delete protected blob data.

### Test

A delete operation was executed from the Azure Container App console using the application's managed identity.

The operation targeted:

`nexaflow-test.txt`

### Expected Result

The delete operation should be denied because the managed identity has read-only blob data access.

### Actual Result

Azure returned:

```text
ErrorCode:AuthorizationPermissionMismatch
Content: <?xml version="1.0" encoding="utf-8"?><Error><Code>AuthorizationPermissionMismatch</Code><Message>This request is not authorized to perform this operation using this permission.
```

### Result

**PASS**

### Security Significance

The managed identity cannot delete protected blob data.

Together, Tests A, B, and C demonstrate that the workload can perform the read operation required by the application while write and delete operations remain unauthorized.

---

## 6. Workload Identity Validation Summary

The workload identity validation was successful.

The Container App managed identity was able to:

- Authenticate to Azure.
- Read the authorized blob resource.

The managed identity was unable to:

- Write blob data.
- Delete blob data.

### Result

**PASS**

### Security Conclusion

The results support the decision to use a system-assigned managed identity with resource-specific Azure RBAC permissions rather than embedded long-lived application credentials.

The demonstrated workload identity is constrained to the minimum tested Azure Storage data-plane permission required by the application.

---

## 7. Test D — Standard User MFA Registration and Authentication

### Objective

Verify that the `NexaFlow Standard User` is protected by multifactor authentication through Microsoft Entra Security Defaults.

### Test

The standard user signed in using its Microsoft Entra user principal name.

Because the account was being used for its first interactive sign-in after a password reset, Microsoft Entra first required the temporary password to be replaced.

Microsoft Entra then required the user to configure Microsoft Authenticator.

The authentication registration process was completed successfully and the user gained access to the Azure portal.

### Expected Result

The standard user should be required to complete an additional authentication factor before accessing Azure management resources.

### Actual Result

Microsoft Entra required Microsoft Authenticator registration and multifactor authentication.

After completing the process, the standard user successfully signed in to the Azure portal.

### Result

**PASS**

### Security Significance

This validates that Security Defaults provides baseline MFA protection for the standard human identity.

### Implementation Note

The legacy Per-user MFA interface displayed the user as `Disabled`.

This did not mean MFA protection was disabled because MFA was being enforced through Security Defaults rather than legacy Per-user MFA.

Custom Conditional Access policies were not implemented because the lab uses Microsoft Entra ID Free.

Conditional Access remains a recommended production enhancement where appropriate licensing is available.

---

## 8. Test E — Standard User Management-Plane Access Denial

### Objective

Verify that the standard-user identity cannot access or manage the NexaFlow Azure environment through the management plane.

### Test

While authenticated as the `NexaFlow Standard User`, the Azure Resource Groups view was opened.

The project resource group:

`rg-nexaflow-identity-demo`

was not visible to the standard user.

A direct URL to the known resource group was then opened.

### Expected Result

The standard user should not be able to access the NexaFlow resource group because no Azure management-plane role had been assigned to the standard-user identity.

### Actual Result

The resource group was not visible.

When direct access was attempted, Azure displayed:

```text
You do not have access
```

### Result

**PASS**

### Security Significance

This validates separation between standard-user authentication and Azure resource-management authorization.

The standard user can authenticate successfully but is not granted unnecessary management-plane permissions.

---

## 9. Test F — Privileged Administrator MFA and Scoped Access

### Objective

Verify that the `NexaFlow Privileged Administrator`:

- Authenticates using multifactor authentication.
- Receives the intended storage-account management access.
- Can read required blob data.
- Cannot modify or delete blob data through its Microsoft Entra data-plane permissions.

---

### 9.1 Privileged Administrator MFA Authentication

The `NexaFlow Privileged Administrator` signed in to the Azure portal.

Microsoft Entra required Microsoft Authenticator as an additional authentication factor.

### Expected Result

The privileged administrator should successfully authenticate using multifactor authentication.

### Actual Result

The privileged administrator successfully completed MFA and accessed the Azure portal.

### Result

**PASS**

---

### 9.2 Storage Management Access

The privileged administrator was able to access the NexaFlow storage account through the assigned:

`Storage Account Contributor`

role.

### Expected Result

The privileged administrator should have management-plane access to the intended storage resource.

### Actual Result

The storage account was accessible to the privileged administrator.

### Result

**PASS**

---

### 9.3 Microsoft Entra Blob Read

The storage portal authentication method was switched to:

`Microsoft Entra user account`

The privileged administrator then opened the NexaFlow blob container and successfully read the test blob.

### Expected Result

The privileged administrator should be able to read blob data through `Storage Blob Data Reader`.

### Actual Result

Blob read access succeeded.

### Result

**PASS**

---

### 9.4 Microsoft Entra Blob Write Denial

During the validation process, a write test was performed using Azure CLI with:

```text
--auth-mode login
```

This forced Azure CLI to use the signed-in Microsoft Entra identity rather than a storage account key.

### Expected Result

The privileged administrator should not be able to upload blob data because `Storage Blob Data Reader` does not grant write permissions.

### Actual Result

Azure returned:

```text
You do not have the required permissions needed to perform this operation.
```

The operation was denied.

### Result

**PASS**

### Security Significance

The privileged administrator's Microsoft Entra data-plane authorization permits read access while preventing unauthorized blob modification.

---

### 9.5 Microsoft Entra Blob Delete Denial

A blob delete operation was also performed using:

```text
--auth-mode login
```

against the existing NexaFlow test blob.

### Expected Result

The privileged administrator should not be able to delete blob data.

### Actual Result

Azure returned:

```text
You do not have the required permissions needed to perform this operation.
```

The delete operation was denied.

### Result

**PASS**

### Security Significance

The privileged administrator cannot delete protected blob data through its assigned Microsoft Entra data-plane permissions.

---

## 10. Security Finding — Shared Key Authorization Path

### Finding

During privileged-access testing, an attempted blob upload unexpectedly succeeded through the Azure portal even though the privileged administrator had only `Storage Blob Data Reader` for blob data.

This triggered further investigation into the effective authorization path.

The `Storage Account Contributor` role provides storage-account management capabilities and permits operations involving the storage account keys.

At the time of the finding, Shared Key authorization was enabled on the storage account.

This introduced an alternate authorization path that could provide broader data access than the intended Microsoft Entra read-only RBAC model.

### Validation

To separate Microsoft Entra authorization from Shared Key authorization, the write and delete operations were repeated using Azure CLI with:

```text
--auth-mode login
```

Both operations were denied.

This confirmed that the Microsoft Entra RBAC path itself was enforcing the intended read-only data permissions.

### Security Significance

The test demonstrated that validating only assigned RBAC roles is not sufficient when alternate authentication mechanisms remain available.

Authentication paths must also be reviewed when evaluating effective access.

---

## 11. Remediation — RBAC Scope and Shared Key Hardening

The security finding resulted in configuration changes.

### 11.1 RBAC Scope Correction

The privileged-administrator role assignments were reviewed and were found to have originally been inherited from the project resource group.

The assignments were corrected so that:

- `Storage Account Contributor`
- `Storage Blob Data Reader`

are scoped specifically to the NexaFlow storage account.

This reduced unnecessary permission scope.

### 11.2 Shared Key Authorization Disabled

Shared Key authorization was disabled on the NexaFlow storage account.

Microsoft Entra authentication became the intended authorization path for blob data access.

### 11.3 Remediation Validation

After the remediation:

- Blob read through Microsoft Entra continued to succeed.
- Blob write through Microsoft Entra was denied.
- Blob delete through Microsoft Entra was denied.

### Remediation Result

**PASS**

### Residual Risk

The privileged administrator retains storage-account management permissions.

An identity with sufficient storage-account management authority may be capable of modifying security-related configuration, including settings associated with Shared Key authorization.

For this project, Shared Key authorization remains disabled.

In a stricter production environment, additional controls could include:

- More restrictive custom administrative roles.
- Separation of duties.
- Azure Policy enforcement.
- Privileged Identity Management.
- Conditional Access for privileged administrators.

These controls are outside the current project scope.

---

## 12. Logging and Auditability Validation

### Objective

Verify that important authentication and Azure management activities are recorded and attributable to the identity that performed them.

The validation used:

- Microsoft Entra sign-in logs.
- Azure Activity Log.

---

### 12.1 Standard User Sign-In Log

The Microsoft Entra sign-in logs were reviewed for:

`NexaFlow Standard User`

### Observed Result

- Status: `Success`
- Authentication requirement: `Multifactor authentication`
- Authentication detail: `MFA requirement satisfied by claim in the token`
- Security Defaults: Present under the authentication/Conditional Access information

### Result

**PASS**

### Security Significance

The sign-in event demonstrates that the standard-user authentication activity is recorded and that MFA was required for the sign-in.

---

### 12.2 Privileged Administrator Sign-In Log

The Microsoft Entra sign-in logs were reviewed for:

`NexaFlow Privileged Administrator`

### Observed Result

- Status: `Success`
- Authentication requirement: `Multifactor authentication`
- Authentication detail: `MFA requirement satisfied by claim in the token`
- Security Defaults: Present under the authentication/Conditional Access information

### Result

**PASS**

### Security Significance

The privileged-administrator authentication activity is recorded and attributable to the appropriate identity.

The logs also confirm that MFA was required.

---

### 12.3 Azure Activity Log — Storage Account Update

The Azure Activity Log recorded the following management-plane operation:

```text
Operation name: Update Storage Account
Status: Succeeded
Event initiated by: adeboyejoeniola@gmail.com
Resource: storageAccounts, nexaflowidentity20260905
Resource group: rg-nexaflow-identity-demo
Time: Thu Sep 10, 2026, 18:48:21 GMT+0100 (West Africa Time)
```

### Result

**PASS**

### Security Significance

This demonstrates that storage-account configuration activity can be traced to the identity that performed the change.

---

### 12.4 Azure Activity Log — Role Assignment

The Azure Activity Log recorded:

```text
Operation name: Create role assignment
Status: Succeeded
Event initiated by: adeboyejoeniola@gmail.com
Resource: storageAccounts, nexaflowidentity20260905
Resource group: rg-nexaflow-identity-demo
Time: Thu Sep 10, 2026, 18:46:30 GMT+0100 (West Africa Time)
```

### Result

**PASS**

### Security Significance

RBAC changes are recorded and attributable to the administrator who performed them.

This provides evidence of administrative accountability for access-control changes.

---

### 12.5 Azure Activity Log — Storage Account Key Activity

The Azure Activity Log also recorded:

```text
Operation name: List Storage Account Keys
Status: Succeeded
Event initiated by: adeboyejoeniola@gmail.com
Resource: storageAccounts, nexaflowidentity20260905
Resource group: rg-nexaflow-identity-demo
Time: Thu Sep 10, 2026, 18:15:13 GMT+0100 (West Africa Time)
```

### Result

**PASS**

### Security Significance

This event is particularly relevant to the Shared Key security finding.

It demonstrates that storage-account key operations are visible in the Azure Activity Log and attributable to the identity that initiated them.

---

## 13. Logging and Auditability Result

The auditability validation was successful.

Microsoft Entra sign-in logs demonstrated:

- Standard-user sign-in visibility.
- Privileged-administrator sign-in visibility.
- Successful authentication status.
- MFA requirements.
- Security Defaults involvement.

Azure Activity Log demonstrated:

- Storage configuration activity.
- RBAC role-assignment activity.
- Storage-account key activity.
- Identity attribution.
- Resource attribution.
- Operation status.
- Timestamp information.

### Result

**PASS**

---

## 14. Overall Security Validation Result

The NexaFlow security validation was successfully completed.

The testing demonstrated:

- Managed identity authentication.
- Authorized workload blob read access.
- Workload write denial.
- Workload delete denial.
- Standard-user MFA enforcement.
- Standard-user management-plane access denial.
- Privileged-administrator MFA enforcement.
- Scoped privileged storage-management access.
- Privileged Microsoft Entra blob read access.
- Privileged Microsoft Entra write denial.
- Privileged Microsoft Entra delete denial.
- Identification of an alternate Shared Key authorization path.
- Remediation of the Shared Key access path.
- Correction of overly broad RBAC scope.
- Human identity sign-in logging.
- Administrative activity logging.
- Identity and resource attribution for management operations.

### Overall Result

**PASS**

---

## 15. Security Conclusion

The NexaFlow implementation demonstrates a layered identity and access model for human users and application workloads.

The application uses a system-assigned managed identity rather than embedded long-lived credentials.

Azure RBAC restricts the workload to the data access required by the application.

Standard users can authenticate through Microsoft Entra but are not granted Azure management-plane privileges.

Privileged users are separated from standard users and receive scoped administrative access.

Microsoft Entra data-plane permissions restrict the privileged administrator to the required blob read access while denying unauthorized write and delete operations.

Security Defaults provides baseline MFA protection for human identities within the limitations of the Microsoft Entra ID Free tenant.

Testing also identified an alternate Shared Key authorization path that could undermine the intended Microsoft Entra RBAC boundary.

The issue was investigated and remediated by disabling Shared Key authorization and validating access again through Microsoft Entra authentication.

Microsoft Entra sign-in logs and Azure Activity Log provide evidence that authentication and administrative activity can be observed and attributed to specific identities.

The project therefore demonstrates not only security configuration, but also:

- Security validation.
- Least-privilege testing.
- Identification of unexpected authorization behavior.
- Root-cause investigation.
- Remediation.
- Retesting.
- Auditability.

---

## 16. Evidence

Evidence captured during the project includes:

- `container-app-running.png`
- `managed-identity-enabled.png`
- `acr-pull-role.png`
- `storage-rbac.png`
- `application-health.png`
- `managed-identity-storage-access.png`

Additional security-testing evidence captured includes:

- Microsoft Authenticator requirement for the standard user.
- Standard-user access denial.
- Privileged-administrator Microsoft Entra write denial in Azure Cloud Shell.
- Privileged-administrator Microsoft Entra delete denial in Azure Cloud Shell.

The evidence is stored in the repository `screenshots/` directory.

---

## 17. Final Test Summary

| Test | Security Control Validated | Result |
|---|---|---|
| Test A | Managed identity authorized blob read | **PASS** |
| Test B | Managed identity unauthorized blob write | **PASS** |
| Test C | Managed identity unauthorized blob delete | **PASS** |
| Test D | Standard-user MFA authentication | **PASS** |
| Test E | Standard-user management-plane denial | **PASS** |
| Test F1 | Privileged-administrator MFA | **PASS** |
| Test F2 | Privileged storage-management access | **PASS** |
| Test F3 | Privileged Entra blob read | **PASS** |
| Test F4 | Privileged Entra blob write denial | **PASS** |
| Test F5 | Privileged Entra blob delete denial | **PASS** |
| Security Finding | Shared Key alternate authorization path identified | **IDENTIFIED** |
| Remediation | RBAC scope corrected | **PASS** |
| Remediation | Shared Key authorization disabled | **PASS** |
| Audit Test | Standard-user sign-in visibility | **PASS** |
| Audit Test | Privileged-admin sign-in visibility | **PASS** |
| Audit Test | Storage configuration activity attribution | **PASS** |
| Audit Test | RBAC role-assignment attribution | **PASS** |
| Audit Test | Storage-account key activity attribution | **PASS** |

---

## 18. Final Project Validation Status

**SECURITY VALIDATION COMPLETE**

All security tests defined for the current NexaFlow project scope were completed successfully.

The implementation has demonstrated:

- Identity-based authentication.
- Least-privilege authorization.
- Human and workload identity separation.
- Privileged-access separation.
- MFA protection.
- Azure RBAC enforcement.
- Alternate authentication-path investigation.
- Security remediation.
- Retesting.
- Logging.
- Auditability.

Remaining work relates to final repository presentation, project documentation review, and Azure resource cost cleanup rather than additional security-control validation.
