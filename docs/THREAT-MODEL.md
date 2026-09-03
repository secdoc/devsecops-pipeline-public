# Threat Model

Artifact ID: DEVSECOPS-PUBLIC-TM-001
Version: 1.0
Classification: Public
Method: threat-informed architecture review using STRIDE categories and NIST SP 800-30 risk-chain language

## Scope and assets

In scope: source integrity, CI execution, dependency retrieval, artifact storage, policy evidence, deployment identity, public mirroring, telemetry, and recovery. Key assets are source, credentials, signing trust, artifacts, SBOMs, approvals, deployment authority, and audit evidence.

Out of scope: adopter-specific network products, identity providers, cloud accounts, application threats, and physical security.

## Trust assumptions

- Contributor code and dependencies may be hostile.
- The build worker may be compromised during a job.
- Protected deployment identity is separate from build identity.
- GitLab is authoritative and GitHub is a downstream public mirror.
- Security telemetry is untrusted input until parsed and normalized.
- Backup restoration requires independent validation.

## Threats and controls

| ID | Threat and risk chain | Primary controls | Residual risk |
|---|---|---|---|
| TM-01 | Malicious merge code compromises a runner, then searches for reusable production credentials | hostile-by-default build plane, no deployment identity, short-lived credentials, cleanup test | runner or kernel escape can affect shared capacity |
| TM-02 | Dependency compromise produces a trusted-looking artifact | approved proxy, pinned inputs, independent scans, SBOM, provenance, review | new or targeted supply-chain attacks may evade scanners |
| TM-03 | Build output is replaced after scanning | immutable digest binding, signature, receipt, deployment-side hash verification | signing trust compromise remains material |
| TM-04 | Severity-only policy creates unsafe exceptions or bypass pressure | exploitability and fixability policy, distinct approver, scoped expiry, reason codes | business pressure can still weaken policy governance |
| TM-05 | Build worker reaches source-control administration, storage, or production | separate planes, default deny, exact allow rules, positive and negative canaries | policy drift can silently widen reachability |
| TM-06 | Public mirror leaks private topology or credentials | fresh public history, positive content boundary, current and history scans, human disclosure review | novel secret forms or contextual disclosure may evade automation |
| TM-07 | GitHub divergence overwrites valid work or creates split authority | one-way mirror, no force push, destination ancestry check, exact OID readback | emergency manual changes require deliberate reconciliation |
| TM-08 | Forged or missing evidence causes unsafe deployment | fail-closed receipt, required scanner versions, exact hashes, protected ref | compromised control plane can forge multiple records |
| TM-09 | Telemetry parser accepts attacker-controlled instructions or fields | schema validation, field allowlists, no direct automation from raw text | semantically valid malicious telemetry remains possible |
| TM-10 | Backup exists but cannot restore the service or decrypt data | encrypted backup, protected decryption material, isolated restore, functional canary | recovery dependencies can share a hidden failure domain |

## Abuse cases to test

- Commit a synthetic secret and require repository validation to reject it.
- Add a private address or internal domain to SVG and require the same rejection.
- Modify an artifact after receipt generation and require deployment verification to fail.
- Use an expired or self-approved exception and require policy denial.
- Attempt publication from a feature branch and require the mirror job to remain absent.
- Create destination divergence and require mirroring to stop without force.
- Remove a required SOC linkage file and require the live integration check to fail.
- Restore a backup into an isolated environment and require a full noncritical pipeline canary.

## Review triggers

Review this model when runner isolation, source authority, signing trust, dependency delivery, deployment identity, mirror direction, evidence format, or backup architecture changes.
