# Pipeline Gates

## Gate order

| Gate | Blocks when | Evidence |
|---|---|---|
| Repository integrity | required governance files or links are missing | validation report |
| Public sanitization | sensitive indicators or malformed public artifacts are found | path, rule ID, reason only |
| Unit and integration tests | tests fail or expected negative behavior is absent | test report |
| Secret detection | Gitleaks, Trivy, or TruffleHog finds a credential or private-key pattern in history, introduced content, or an immutable snapshot | allowlisted report with no candidate value, plus source revision or snapshot digest |
| SAST and IaC | policy-defined blocking findings exist | normalized finding inventory |
| Dependency and image analysis | critical, KEV, or fixable high findings violate policy | scanner versions, database age, finding IDs |
| SBOM | SBOM is missing, malformed, or not bound to artifact digest | SBOM hash and artifact hash |
| Policy | exception invalid, expired, self-approved, or finding is unhandled | reason-coded decision |
| Signature and provenance | release artifact cannot be verified | signature and attestation verification |
| Deployment authorization | ref, environment, identity, digest, or target mismatches | protected job receipt |
| Public mirror | tree is unsanitized or GitHub has diverged | exact source and destination refs |

## Default risk policy

- Critical vulnerabilities block.
- Known-exploited vulnerabilities block regardless of severity.
- Fixable High vulnerabilities block.
- Missing or malformed evidence blocks.
- Unfixed High, Medium, and Low findings remain visible unless local policy raises the threshold.
- Exceptions must match scanner, vulnerability, component, and artifact digest. They need distinct owner and approver identities and a future expiry.

## Failure behavior

A failed gate does not advance delivered state, publish an artifact, deploy, or mirror. Retries operate on the same immutable input. A human exception cannot replace missing evidence or bypass digest mismatch.

TruffleHog provider verification is disabled in the untrusted pipeline. The control must fail closed on findings, malformed JSON, scanner errors, or an inconsistent exit code. Only the sanitized summary is retained. Raw scanner output is temporary and must not enter artifacts, logs, telemetry, or release receipts.

## Receipt contract

A release receipt contains the source revision, artifact hash, SBOM hash, scanner versions, normalized findings, policy result, exception IDs, and creation time. The deployment worker recalculates hashes before activation.
