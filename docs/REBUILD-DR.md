# Rebuild and Disaster Recovery

## Recovery inputs

- tested backups of GitLab repositories, database, LFS, registry, packages, and configuration
- protected application secrets required to decrypt restored data
- runner definitions and rebuild automation, without reusable job credentials
- policy, exception, signing, and trust-root records
- DNS, PKI, identity, telemetry, and network contracts
- repository-scoped GitHub mirror key registration records, not plaintext private keys in documentation

## Ordered rebuild

1. Recreate the control-plane host on a supported OS and apply the owner-access baseline.
2. Restore DNS, time, PKI trust, and identity dependencies.
3. Restore GitLab configuration and secrets, then application data, repositories, LFS, registry, and packages.
4. Verify owner and break-glass access, protected refs, project visibility, audit events, and exact repository heads.
5. Restore dependency services and verify package and vulnerability database freshness.
6. Rebuild build workers from code. Register new project-scoped identities and rerun positive and negative reachability tests.
7. Rebuild protected deployment workers separately. Reissue short-lived trust and verify exact targets.
8. Run a noncritical pipeline through test, SBOM, scan, policy, signature, provenance, and deployment rejection tests.
9. Restore the public mirror identity. Verify the GitHub destination has not diverged before resuming.
10. Run a complete isolated restore exercise and record RTO, RPO, gaps, and rollback evidence.

## Acceptance

Recovery is not complete when services merely start. Require repository integrity, registry pulls by digest, valid SBOM and policy evidence, runner cleanup, target authorization, telemetry, backup scheduling, an isolated restore, and public mirror ref parity.

## Untested boundaries

This public reference cannot test an adopter's identity provider, network enforcement, storage, PKI, signing trust root, production targets, or backup platform. Those remain local acceptance gates.
