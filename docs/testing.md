# Security Testing — NexaFlow

## 1. Purpose

This document records the security validation performed for the NexaFlow customer identity platform.

The testing focused on validating that the application's system-assigned managed identity has the minimum Azure Storage permissions required by the workload.

The primary validation goal was to confirm:

- Authorized application read access succeeds.
- Unauthorized write access is denied.
- Unauthorized delete access is denied.

---

## 2. Test Environment

- Azure subscription: Pay-As-You-Go
- Microsoft Entra ID: Free
- Security Defaults: Enabled
- Resource group: `rg-nexaflow-identity-demo`
- Container App: `nexaflow-identity-app`
- Storage Account: NexaFlow demonstration storage account
- Blob container: `nexaflow-test-data`
- Workload identity: System-assigned managed identity
- Workload identity storage role: `Storage Blob Data Reader`

---

## 3. Test A — Authorized Blob Read

### Objective

Verify that the Container App can use its managed identity to access an authorized Azure Storage blob.

### Test

The application endpoint `/data` was accessed through the deployed Container App.

### Expected Result

The application should successfully authenticate to Azure and read the test blob without using a storage account key or connection string.

### Actual Result

The application successfully retrieved the test blob.

### Result

**PASS**

### Security Significance

This confirms that the application workload identity has the required access to the protected storage data.

---

## 4. Test B — Unauthorized Blob Write

### Objective

Verify that the application workload identity cannot write blob data beyond its assigned permissions.

### Test

An upload operation was executed from the Container App console using the workload's managed identity.

### Expected Result

The operation should be denied because the workload identity has `Storage Blob Data Reader`, which does not provide blob write permission.

### Actual Result

The operation returned:

```text
ErrorCode:AuthorizationPermissionMismatch
Content: <?xml version="1.0" encoding="utf-8"?><Error><Code>AuthorizationPermissionMismatch</Code><Message>This request is not authorized to perform this operation using this permission.
```

## 5. Test C — Unauthorized Blob Delete

### Objective

Verify that the application workload identity cannot delete blob data.

### Test

A delete operation was executed from the Container App console using the workload's managed identity against the existing test blob.

### Expected Result

The operation should be denied because the workload identity has read-only blob data permissions.

### Actual Result

The operation returned:

```text
ErrorCode:AuthorizationPermissionMismatch
Content: <?xml version="1.0" encoding="utf-8"?><Error><Code>AuthorizationPermissionMismatch</Code><Message>This request is not authorized to perform this operation using this permission.
```

### Result

**PASS**

### Security Significance

The workload identity cannot delete protected blob data, further demonstrating least-privilege enforcement.

---

## 6. Overall Validation Result

The workload identity security validation was successful.

The application was able to:

- Authenticate using its managed identity.
- Read the authorized blob resource.

The application was unable to:

- Write blob data.
- Delete blob data.

This demonstrates that the workload identity is restricted to the minimum demonstrated data-plane permission required by the application.

---

## 7. Security Conclusion

The validation supports the NexaFlow design decision to use a system-assigned managed identity with resource-specific Azure RBAC permissions instead of embedded long-lived application credentials.

The demonstrated access model separates required application access from unauthorized modification and deletion privileges.

The testing specifically demonstrates that the application workload identity is correctly authenticated and constrained by least-privilege Azure Storage RBAC.

---

## 8. Evidence

Relevant evidence is stored in the repository `screenshots/` directory.

- `managed-identity-enabled.png`
- `storage-rbac.png`
- `managed-identity-storage-access.png`
