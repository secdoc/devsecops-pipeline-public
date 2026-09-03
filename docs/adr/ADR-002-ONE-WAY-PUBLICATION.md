# ADR-002: GitLab Authority and One-Way GitHub Publication

Status: Accepted
Date: 2026-09-03 UTC

## Context

The project needs a public collaboration and availability surface without creating two authoritative histories or exposing private operational repositories.

## Decision

GitLab is authoritative. GitHub receives a sanitized, one-way branch and tag mirror after all gates pass. The public repository starts with fresh history and never inherits private repository history. Destination divergence fails closed and is reconciled through GitLab.

## Consequences

GitHub pull requests cannot merge directly into the authoritative branch. Contributors may propose changes on GitHub, but maintainers apply accepted changes through GitLab. Repository-scoped deploy keys increase key-management work but avoid a broad portfolio token.
