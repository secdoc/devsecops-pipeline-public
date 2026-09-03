# Tool Selection Decisions

The design uses replaceable stage roles. Tools are selected for the reference implementation, but the interfaces and security properties matter more than brands.

| Stage | Reference tool | Why selected | Cost or limitation | Acceptable alternative |
|---|---|---|---|---|
| Source and CI | GitLab CE | self-hosted source, registry, CI, protected refs | custom integration is needed for some security features | GitHub Enterprise, Forgejo plus CI |
| Build isolation | project-scoped runner with rootless container engine | limits cross-project and host exposure | more cleanup and capacity work | ephemeral VM runner, Kubernetes executor |
| Package proxy | Nexus Repository | multi-ecosystem proxying and policy point | backup and upgrade burden | Artifactory, cloud artifact service |
| SBOM | Syft | broad format support and CycloneDX output | package detection varies by ecosystem | CycloneDX native plugins, Trivy SBOM |
| Vulnerability scan | Grype plus Trivy | independent views and SBOM scanning | database delivery and finding differences | enterprise SCA scanner |
| SAST | Semgrep | accessible custom rules and broad language support | community rules require tuning | CodeQL, SonarQube, commercial SAST |
| IaC | Checkov | broad IaC coverage and CLI integration | policy noise requires baselining | Trivy config, tfsec, OPA/Conftest |
| SBOM inventory | Dependency-Track | portfolio visibility and CycloneDX analysis | ingestion is asynchronous | DefectDojo, commercial SCA portal |
| Signing | Cosign | OCI and keyless or key-backed signing | trust-root design remains required | Notary v2 ecosystem, cloud signer |
| Secrets | Vault | short-lived workload identity and policy | outage and recovery complexity | cloud workload identity and secret manager |
| Telemetry | Wazuh and Graylog role pattern | endpoint detection plus transport and retention | parser and HA operations | other SIEM and log platforms |
| Public mirror | repository-scoped SSH deploy key | narrow write scope and independent revocation | one key per repository | GitLab native push mirror where licensed |

## Rejected shortcuts

- A single runner for build and production deployment.
- Direct Internet access from every job.
- Host Docker socket mounts for untrusted jobs.
- Rebuilding an artifact in each environment.
- Long-lived production secrets in project variables.
- Severity-only gates with no exploitability, fixability, or exception lifecycle.
- Bidirectional GitLab and GitHub synchronization.
