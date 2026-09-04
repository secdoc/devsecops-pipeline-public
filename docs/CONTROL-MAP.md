# Control Map

This mapping uses NIST SP 800-218 SSDF v1.1 as the software-delivery backbone and NIST SP 800-53 Rev. 5 for supporting controls. It is not an attestation.

| Control | Reference implementation | Evidence | Residual risk |
|---|---|---|---|
| SSDF PO.1 | versioned security requirements and release policy | policy file and reviewed changes | service-specific requirements remain local |
| SSDF PO.3 | integrated test, SAST, SCA, IaC, SBOM, signing, and provenance stages | pipeline jobs and receipt | scanner coverage is incomplete |
| SSDF PO.5 | separate control, build, and deployment planes | network and identity tests | segmentation errors can bypass intent |
| SSDF PS.1 | protected refs, least privilege, monitored break-glass | access and branch exports | local accounts require review |
| SSDF PS.2 | digest, signature, SBOM, and provenance verification | release receipt | trust-root compromise remains material |
| SSDF PW.4 | approved proxies and dependency analysis | proxy logs and SBOM | upstream compromise remains possible |
| SSDF PW.6 | pinned builds and cleanable workers | runner configuration and cleanup test | some ecosystems need exceptions |
| SSDF PW.7 | review, SAST, Gitleaks, Trivy, multi-stage TruffleHog secret detection, and IaC checks | source-revision and snapshot-digest-bound sanitized pipeline evidence | false positives and legacy history need ownership |
| SSDF PW.8 | unit, integration, and negative tests | test reports | testing cannot prove absence of defects |
| SSDF RV.1 and RV.2 | independent scans and risk-based policy | findings and decision receipt | data freshness affects decisions |
| AC-6 | separate identities and exact target access | authorization tests | mis-scoped identity can bypass network controls |
| AU-2 and AU-12 | pipeline, registry, deploy, and deny telemetry | SIEM events and feed-silence alerts | telemetry loss can hide activity |
| CM-3 | merge review, policy change control, and rollback | Git history and approvals | emergency work needs retrospective review |
| CP-9 and CP-10 | encrypted backup and isolated restore | restore acceptance record | snapshots alone are insufficient |
| IA-5 | short-lived workload credentials and rotation | secret-manager audit | bootstrap material remains sensitive |
| SC-7(5) | default-deny boundaries with exact exceptions | positive and negative canaries | stateful-policy behavior varies by platform |
| SR-3 and SR-4 | approved sources, SBOM, signatures, and provenance | supply-chain receipt | transitive dependencies remain a risk |
