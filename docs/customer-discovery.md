# Customer Discovery — NexaFlow

## 1. Business Context

NexaFlow is a growing B2B SaaS company with approximately 80 employees. The company is preparing to launch a customer-facing application and expects its business and customer base to grow.

As the organization has grown rapidly, its identity and access practices have developed informally. NexaFlow now wants to establish a more structured and secure identity and access model before the application is launched and the company begins onboarding larger customers.

## 2. Current Problems

NexaFlow currently has several identity and access challenges:

Employees may have access to resources beyond what they require for their roles.
Administrative users are not sufficiently separated from normal users.
MFA is not consistently enforced.
Application access needs to be controlled according to identity and security conditions.
The development team needs the application to access Azure resources without storing credentials in application code.
Security leadership lacks sufficient visibility into sign-in and access activity.
The organization does not yet have a clearly documented identity and security model that can support future growth.


## 3. Business Risks
If these issues remain unresolved, NexaFlow could face:

Increased risk of compromised user accounts.
Unauthorized access to applications and cloud resources.
Exposure of sensitive business or customer data.
Greater risk from excessive privileges.
Difficulty investigating suspicious identity activity.
Potential customer-trust and reputational consequences following a security incident.
Increased difficulty meeting the security expectations of larger customers.
Greater operational complexity as the company continues to grow.

## 4. Stakeholders

IT / Identity administrators — responsible for identity and access management.
Application development team — responsible for the customer-facing application and its access to Azure resources.
Standard employees — require appropriate access to business resources.
Business leadership — concerned with growth, customer trust, operational efficiency and risk.
Security leadership — concerned with risk reduction, visibility and security controls.


## 5. User Types

For this project, I identify three primary identity categories:

Standard employees
Employees who require access to business applications and resources necessary for their roles.
Administrators
Privileged users who require elevated access to manage identity, security and Azure resources.
Application / workload identity
The customer-facing application requires its own identity to authenticate to Azure resources without depending on a human user's credentials.

## 6. Functional Requirements

The solution should allow:

Users to authenticate securely.
Access to resources to be assigned according to roles and responsibilities.
Administrators to perform required privileged tasks.
The application to authenticate to Azure resources without embedded credentials.
Security personnel to view relevant identity and access activity.
Access decisions to be influenced by security and identity conditions.

## 7. Security Requirements
The solution should:

Enforce MFA where required.
Apply Conditional Access policies.
Follow the principle of least privilege.
Separate privileged access from standard user access.
Use appropriate RBAC roles.
Avoid storing long-lived credentials or secrets in application code.
Provide visibility into authentication and access activity.
Provide controls for detecting or preventing access that does not satisfy security requirements.

## 8. Technical Requirements
The solution should make appropriate use of:

Microsoft Entra ID for identity.
RBAC for authorization to Azure resources.
Conditional Access for identity-based access controls.
Managed identity for application-to-Azure authentication where supported.
Azure monitoring/logging capabilities for identity and access visibility.

Important: At this stage, these are potential technical capabilities based on the stated requirements. The final architecture and specific services should be validated after the requirements and threat analysis.

## 9. Operational Requirements
NexaFlow needs a solution that is:

Easy enough to administer for a growing organization.
Scalable as the company adds employees and customers.
Auditable.
Documented.
Capable of supporting security investigations.
Designed to minimize unnecessary operational complexity.

## 10. Constraints

For this project:

The implementation should be cost-conscious.
Only the resources necessary to demonstrate the required capabilities should be deployed.
The solution should avoid unnecessary recurring costs.
Billable resources should be minimized or removed when testing is complete.
The design should remain realistic enough to demonstrate how the solution could evolve as NexaFlow grows.

## 11. Assumptions
Because this is a simulated customer engagement, I am making several assumptions:

NexaFlow primarily uses Microsoft Azure.
The company has approximately 80 employees.
Employees have different responsibilities and therefore should not automatically receive identical permissions.
A subset of users requires administrative privileges.
The customer-facing application will run on Azure.
The application needs to access Azure resources programmatically.
Security leadership wants improved identity visibility and auditability.
NexaFlow wants to establish a more mature security model before significant customer growth.

## 12. Success Criteria

The project will be considered successful when NexaFlow can demonstrate that:

Standard users receive only the access required for their roles.
Privileged users have stronger access controls.
MFA and Conditional Access policies enforce the intended authentication requirements.
The application can access required Azure resources using a managed identity rather than embedded credentials.
Unauthorized access attempts are appropriately blocked or restricted.
Relevant identity and access activity is visible through logging/monitoring.
The identity and security architecture is documented.
The solution provides a foundation that can scale with NexaFlow's growth.

## 13. Out of Scope

The following are intentionally excluded from this project:

Enterprise Identity Governance platforms such as SailPoint or Saviynt
Third-party IAM platforms such as Okta
Full enterprise SIEM/SOC implementation
Production-scale disaster recovery
Multi-region architecture
Full production customer identity federation
Enterprise privileged access management platform deployment

## 14. Security Assumptions

Privileged administrators represent a small subset of NexaFlow employees.
Privileged access should be more restrictive than standard employee access.
Human users and application workloads should have separate identities.
Long-lived application credentials should be avoided where managed identity is supported.
Access should follow least-privilege principles.
Security-relevant authentication and access activity should be available for investigation.

## 15. Data Considerations

The customer-facing application is assumed to process business and customer information that should not be accessible to unauthorized identities.

The solution should protect:

Customer/application data
Authentication information
Application secrets and keys
Administrative configuration
Security and audit information

## 16. Privileged Access Requirements

Administrative access must be separated from standard employee access.
Privileged roles should be assigned only where required.
Privileged actions should use stronger authentication controls.
Administrative access should be auditable.
Privileged permissions should be removable when no longer required.

## 17. Security Validation Scenarios

### Scenario 1 — Standard User Attempts Privileged Access
    Expected: Access is denied.

### Scenario 2 — Privileged User Without Required Authentication Condition
    Expected: Access is blocked or restricted according to policy.

### Scenario 3 — Application Attempts Unauthorized Resource Access
    Expected: Access is denied.

### Scenario 4 — Application Accesses Authorized Resource
    Expected: Access succeeds.

### Scenario 5 — Identity Activity Is Generated
    Expected: Relevant activity can be identified in available logs.
