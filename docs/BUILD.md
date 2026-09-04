# Build and Adoption Guide

## Prerequisites

- GitLab project with protected default branch
- at least one isolated build worker
- a separate protected deployment worker
- private registry or artifact store
- package and vulnerability-data proxying when runners lack Internet access
- secret manager capable of short-lived workload identity
- centralized security telemetry
- backup storage that runners cannot access

## Build sequence

1. Create control, build, and deployment trust boundaries. Use example address space from RFC 5737 documentation ranges in public designs. Select real addressing only in private implementation records.
2. Deploy GitLab and registry services in the control plane. Configure owner access, monitored break-glass access, TLS, backup, and audit forwarding.
3. Register one project-scoped build worker. Do not mount the host container socket. Confirm negative reachability to management, storage, control host administration, and deployment targets.
4. Add dependency proxying and pinned build images. Treat scanner image delivery and vulnerability database delivery as separate dependencies.
5. Configure tests, secret detection, SAST, software-composition analysis, IaC checks, container scanning, SBOM generation, policy evaluation, and evidence retention.
6. Build once. Record the artifact digest before scanning. Bind the completed SBOM, scan results, exceptions, signature, and provenance to that digest.
7. Deploy a separate protected worker. Grant access only to approved artifacts, the exact target, and short-lived deployment identity.
8. Prove deployment rejects an altered artifact, altered receipt, unprotected ref, expired exception, and unauthorized target.
9. Configure encrypted backups and run an isolated restore.
10. Configure one-way GitLab-to-GitHub mirroring only after the public tree passes sanitization.

## Repository validation

```bash
python3 scripts/render_architecture.py
python3 -m unittest discover -s tests -v
python3 scripts/validate_repository.py .
```

The validator checks tracked content for private keys, certificates, token patterns, internal domain suffixes, private addressing, live VM identifiers, malformed JSON, invalid SVG, missing diagram accessibility elements, broken relative links, and required governance files.

## GitLab CI setup

Copy `.gitlab-ci.yml` into the authoritative GitLab project. Assign jobs to isolated runners using your own tags. Protect the mirror job and configure:

- `GITHUB_MIRROR_URL`: SSH destination such as `git@github.com:ORG/REPO.git`
- a repository-scoped GitHub deploy key available only to the protected mirror worker
- pinned GitHub host keys on the mirror worker

Do not store a broad GitHub personal access token on a general build runner.

The local `.gitlab/security-toolchain.yml` adapter adds full-history Gitleaks, Trivy filesystem scanning, Semgrep, Checkov, Syft CycloneDX generation, ClamAV, and TruffleHog scans of Git history and the immutable repository snapshot. Set `SECURITY_TOOLCHAIN_READY=true` only on a runner where every command and an approved `SEMGREP_RULESET` are available. Set `TRUFFLEHOG_VERSION` to the exact reviewed scanner version and pin the installed binary, package, or OCI image in local runner automation. The jobs fail if a command, version declaration, or required input is absent. Keep the variables unset rather than pretending unavailable tools passed, and make the jobs required before production adoption.

TruffleHog runs with provider verification disabled. Raw JSONL exists only in a mode-0600 temporary file and is removed by an exit trap. `scripts/trufflehog_report.py` retains only detector identity, verification state, file, line, commit, scope, scanner version, digest binding, and counts. Never retain TruffleHog `Raw`, `RawV2`, `SecretParts`, `ExtraData`, or candidate values as CI artifacts or logs.

## Linked SOC project

`integrations/soc-pipeline-public.json` links the delivery-plane reference to the public SOC reference. Run:

```bash
python3 scripts/verify_linkage.py --live
```

The live check requires approved Internet access. Offline CI still validates the integration manifest schema and expected URL.

## Acceptance

Acceptance requires successful local tests, repository validation, current diagrams generated from specs, live link verification, GitLab pipeline success at the exact commit, mirror readback showing the same Git commit, and independent GitHub Actions success.
