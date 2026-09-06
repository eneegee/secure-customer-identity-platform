# Architecture Decision — NexaFlow

## 1. Decision Context

NexaFlow has grown rapidly to approximately 80 employees, and its identity and access practices have developed informally as the organization has expanded. The company is preparing to launch a customer-facing application and therefore needs stronger controls around user access, privileged identities, and application access to Azure resources. Existing weaknesses such as excessive permissions, inconsistent MFA, limited visibility into identity activity, and the use of application credentials create unnecessary security risk. NexaFlow therefore needs a scalable identity and security architecture that improves protection and auditability without introducing unnecessary cost or operational complexity.

---

## 2. Requirements Driving the Decision

### 1. Strong authentication

The solution should enforce stronger authentication controls, including MFA, to reduce the risk of compromised credentials.

### 2. Least-privilege access

Users, administrators, and application workloads should receive only the permissions required for their responsibilities.

### 3. Privileged-access separation

Administrative access should be appropriately separated from normal employee access and subject to stronger controls.

### 4. Secure workload identity

The application should be able to authenticate to Azure resources without relying on long-lived credentials or storing secrets in application code.

### 5. Controlled authorization

Access to applications and Azure resources should be based on identity, role, and applicable security conditions.

### 6. Auditability and visibility

Authentication, access, and relevant administrative activity should be visible through appropriate logging so that security activity can be reviewed and investigated.

### 7. Scalability

The architecture should support NexaFlow's expected growth in employees, applications, and customers without requiring a complete redesign.

### 8. Cost and operational simplicity

The solution should provide an appropriate level of security while avoiding unnecessary licensing, infrastructure cost, and administrative complexity.

---

## 3. Architecture Options Considered

### Option A — Basic Entra ID + Azure RBAC

This option would provide a basic identity and authorization foundation using Microsoft Entra ID and Azure RBAC. It would address fundamental identity management and resource authorization requirements while remaining relatively simple and cost-conscious.

However, it would not sufficiently address NexaFlow's need for stronger authentication controls, conditional access, workload identity, privileged-access separation, and broader identity activity visibility. Several important security requirements would therefore remain only partially addressed.

**Advantages:**

- Simple architecture
- Lower operational complexity
- Lower cost
- Provides foundational identity and authorization

**Limitations:**

- Limited authentication controls
- Limited conditional access capability
- Weaker privileged-access model
- Less complete coverage of NexaFlow's security requirements

---

### Option B — Enhanced Azure Identity Architecture

This option combines Microsoft Entra ID, Azure RBAC, MFA, Conditional Access, managed identity, privileged-access separation, and identity/activity logging.

It addresses the majority of NexaFlow's stated requirements while remaining based primarily on Azure-native capabilities. It provides stronger security than Option A without introducing the complexity of an enterprise IAM/PAM platform that may be disproportionate to an 80-person organization.

**Advantages:**

- Strong coverage of core security requirements
- Supports least privilege
- Stronger user authentication
- Supports workload identity
- Better privileged-access separation
- Improved auditability
- Scalable as the company grows
- Relatively low architectural complexity
- Appropriate for a cost-conscious implementation

**Limitations:**

- More configuration and administration than Option A
- Some advanced identity capabilities may depend on licensing
- Requires careful policy design to prevent access disruption
- Does not provide the complete feature depth of specialized enterprise IAM/PAM platforms

---

### Option C — Enterprise IAM/PAM-heavy Architecture

This option would introduce a more comprehensive identity and privileged-access architecture, potentially including advanced governance, access certification and enterprise PAM capabilities.

It could provide stronger control over complex identity environments and privileged access. However, for an 80-person growing SaaS company, the additional operational overhead, implementation complexity and potential licensing cost would likely exceed the current requirements.

This option may become appropriate as NexaFlow grows, enters more heavily regulated markets, or develops more demanding customer and governance requirements.

**Advantages:**

- Strong identity governance
- Strong privileged-access management
- More advanced lifecycle and access governance
- Suitable for complex enterprise environments

**Limitations:**

- Higher cost
- Greater operational complexity
- Longer implementation effort
- Potentially disproportionate to NexaFlow's current size and requirements

---

## 4. Option Comparison

| Requirement | Option A — Basic Entra ID + RBAC | Option B — Enhanced Azure Identity Architecture | Option C — Enterprise IAM/PAM |
|---|---|---|---|
| Strong authentication | Partial | **Strong** | Strong |
| Least privilege | Partial | **Strong** | Strong |
| Privileged-access separation | Limited | **Good** | Strong |
| Secure workload identity | Limited | **Strong** | Strong |
| Controlled authorization | Good | **Strong** | Strong |
| Auditability | Partial | **Good** | Strong |
| Scalability | Good | **Strong** | Strong |
| Cost efficiency | **Strong** | Good | Weak |
| Operational simplicity | **Strong** | Good | Weak |
| Fit for current NexaFlow needs | Moderate | **Strong** | Low–Moderate |
| Overall suitability | Moderate | **Best fit** | Excessive for current scope |

---

## 5. Recommended Architecture

**Option B — Enhanced Azure Identity Architecture** is recommended.

The proposed architecture will use Microsoft Entra ID as the central identity foundation, Azure RBAC for authorization, MFA and Conditional Access for stronger authentication and access decisions, managed identity for application-to-Azure authentication, and Azure identity/activity logging for visibility and investigation.

The design will separate standard-user access from privileged administrative access and will apply least-privilege principles to both human and workload identities.

---

## 6. Why This Architecture

Option B provides the best balance between **security, scalability, operational complexity and cost** for the current NexaFlow scenario.

It directly addresses the major risks identified during the threat-modeling exercise:

- Compromised employee accounts
- Compromised privileged identities
- Excessive permissions
- Workload credential exposure
- Unauthorized application/resource access
- Limited identity visibility
- Security-policy tampering

It also aligns closely with the recurring market requirements identified from the job-description dataset, particularly:

**Entra/IAM, RBAC, MFA, Conditional Access, privileged access, least privilege, workload identity, Zero Trust, monitoring, documentation and troubleshooting.**

The architecture is also intentionally extensible. NexaFlow can introduce more advanced governance or privileged-access capabilities later without requiring the identity foundation to be completely redesigned.

---

## 7. Security Trade-offs

The recommended architecture improves security substantially compared with the basic identity model, but it introduces additional policy and administration requirements.

### Stronger controls vs simplicity

MFA and Conditional Access improve protection against identity compromise but introduce additional authentication conditions that must be designed carefully to avoid unnecessarily disrupting legitimate users.

### Least privilege vs operational convenience

Restricting permissions reduces the potential impact of compromised accounts, but users and applications may occasionally require additional permissions. Access therefore needs to be reviewed and adjusted based on justified business requirements.

### Privileged separation vs administrator convenience

Separating privileged activity from normal access improves security but may require administrators to use additional authentication or privileged-access workflows.

### Managed identity vs compatibility

Managed identity reduces reliance on long-lived credentials, but it is only applicable where the Azure service and application architecture support it.

### Logging vs cost

Increasing logging improves investigation capability but excessive telemetry can create unnecessary monitoring costs. The project therefore uses only the logging necessary to demonstrate the required security and audit capabilities.

### Privileged Storage Access

The privileged administrator will use a resource-specific management role rather than the broader Azure Contributor role. Storage Account Contributor provides management-plane access to the NexaFlow storage account, while Storage Blob Data Reader provides read-only access to the stored data.

This separation limits unnecessary permissions while still allowing the administrator to perform the management and validation activities required for this project.

---

## 8. Cost Trade-offs

The architecture is intentionally designed around **low-cost Azure-native capabilities**.

The project will avoid unnecessary deployment of expensive enterprise services simply to reproduce capabilities that can be demonstrated through lower-cost alternatives.

The implementation will prioritize:

- Consumption-based services where appropriate
- Small test resources
- Minimal logging volumes
- Limited test identities
- Short-lived deployments
- Removal of billable resources after testing

Advanced enterprise IAM, third-party governance platforms and full enterprise SIEM/PAM solutions are intentionally excluded from the core implementation.

This represents a distinction between:

> **what is appropriate for a portfolio demonstration**

and:

> **what might be appropriate in a larger production environment.**

A production environment with greater risk, regulation or scale could justify additional security services and licensing.

### Entra Licensing Constraint

The current project environment uses Microsoft Entra ID Free. Security Defaults can provide baseline MFA protection, but customized Conditional Access policies require Microsoft Entra ID P1 or an eligible qualifying license.

Because this is a cost-conscious personal project, the core implementation will use the security capabilities available in the current tenant rather than purchasing a premium identity license solely for the demonstration.

For a production NexaFlow environment, Microsoft Entra ID P1 or an eligible qualifying license would be evaluated to implement customized Conditional Access policies aligned with the organization's risk and access requirements.

---

## 9. Limitations

This project is a **simulated customer scenario implemented in a personal learning environment**.

It does not demonstrate:

- Production identity administration
- Enterprise-scale IAM governance
- Production PAM operations
- Production incident-response experience
- Large-scale access certification
- Enterprise regulatory audit ownership
- Production availability or business continuity

The implementation is intentionally smaller than a real enterprise deployment.

It demonstrates the ability to reason about and implement a representative identity-security architecture, not professional production experience.

### Conditional Access Limitation

Custom Conditional Access policies are not implemented in the current environment because the tenant has Microsoft Entra ID Free. The project will instead demonstrate the available MFA/security-default capabilities and document Conditional Access as a production recommendation.

---

## 10. Decision

**Decision: Proceed with Option B — Enhanced Azure Identity Architecture.**

The architecture provides the strongest balance between NexaFlow's security requirements, expected growth, operational simplicity and cost constraints.

The implementation will therefore focus on:

```text
Microsoft Entra ID
        ↓
MFA + Conditional Access
        ↓
RBAC + Least Privilege
        ↓
Privileged Access Separation
        ↓
Application / Managed Identity
        ↓
Azure Resource Authorization
        ↓
Identity & Activity Logging
