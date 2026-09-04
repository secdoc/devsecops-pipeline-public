# Operations and Rollback

## Routine operations

- Review failed gates by reason code. Do not rerun until inputs or policy change.
- Keep scanner databases, package proxies, and build images current through controlled updates.
- Review protected branches, runner scope, deployment identities, and exceptions at least quarterly.
- Monitor runner cleanup, denied network flows, pipeline failures, mirror failures, backup age, and restore-test age.
- Reconcile GitLab and GitHub branch and tag maps after every mirror run.
- Confirm each TruffleHog summary is bound to the expected source revision or snapshot digest and contains no raw candidate-secret fields.

## Upgrades

1. Record current versions, backups, and a rollback point.
2. Test the upgrade against a noncritical project.
3. Verify source, registry, runner, policy, mirror, backup, and restore behavior.
4. Upgrade one stateful component at a time.
5. Keep the prior supported version and immutable backup until the hold period passes.

For a TruffleHog upgrade, pin the replacement build, run clean and synthetic-finding canaries against both history and snapshot jobs, verify exit-code handling, inspect the retained ZIP contents, and confirm raw candidate material is absent before promotion.

## Mirror incident

If GitHub diverges, stop the mirror. Do not force-push. Determine whether the destination contains a legitimate contribution, an unauthorized write, or an automation error. Apply accepted changes through GitLab, then resume only after source ancestry and destination ref maps are reconciled.

## Credential incident

Disable the affected credential first. Preserve non-secret audit evidence, rotate through the secret manager, update only the authorized consumer, verify the replacement, and remove the old credential. If a credential reached Git history, assume compromise even after history rewriting.

Do not use TruffleHog provider verification to decide whether rotation is required. A committed candidate is handled as exposed. Rotate first, then purge history where appropriate, then correct the preventive control.

## Rollback

- Pipeline policy: revert the GitLab commit and rerun validation. Do not modify evidence from a prior decision.
- TruffleHog adapter: disable only through a reviewed revert, preserve prior sanitized summaries, remove temporary raw files, and keep Gitleaks and Trivy active while the scanner path is repaired.
- Runner: disable assignment, revoke identity, preserve logs, destroy or clean the workspace according to the runner model, then prove no residual credentials remain.
- Deployment: activate the last accepted immutable digest using the same receipt checks.
- Public mirror: disable the timer or mirror job and revoke its repository deploy key. GitLab remains authoritative.

## Boundaries

Rollback must not reactivate retired systems, weaken protected refs, enable shared runners, grant broad network access, or convert a failed release into an approved one.
