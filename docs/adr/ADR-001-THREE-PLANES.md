# ADR-001: Separate Control, Build, and Deployment Planes

Status: Accepted
Date: 2026-09-03 UTC

## Context

CI executes contributor and dependency-controlled code. Source control stores high-value intellectual property and authorization state. Deployment workers need narrow access to application environments.

## Decision

Use separate control, build, and deployment planes with separate machine identities and authorization. The security platform observes all three and does not route traffic between them.

## Consequences

Compromise of a build job has a smaller path to source-control administration or production. The design costs more hosts, firewall policy, identity lifecycle, and recovery testing. That cost is accepted because a shared build and deployment worker collapses the most important trust boundary.
