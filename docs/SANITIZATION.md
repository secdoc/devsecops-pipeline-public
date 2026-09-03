# Public Sanitization Contract

## Publication rule

Public content is authored as a safe reference. It is not produced by copying private repositories and replacing a few strings. Files containing live evidence, topology, identity, or recovery material are excluded at the source boundary.

## Prohibited content

- passwords, tokens, cookies, API keys, recovery codes, private keys, or encrypted secret blobs
- certificates, public-key fingerprints, pinned server keys, or credential-bearing URLs
- internal DNS suffixes and nonpublic service URLs
- private IPv4 or IPv6 addresses, MAC addresses, serial numbers, VM IDs, VLAN IDs, and device identifiers
- real usernames, directory groups, email addresses other than the repository attribution address
- live firewall policies, routing tables, asset inventories, backups, scanner output, logs, screenshots, and acceptance evidence
- exploit-enabling detail about current defensive gaps or management paths

## Safe substitutions

Use role names such as `git.example.invalid`, `registry.example.invalid`, and `deploy-worker`. Use RFC 5737 networks (`192.0.2.0/24`, `198.51.100.0/24`, and `203.0.113.0/24`) only when addresses add value. Use synthetic artifacts and clearly label proposed versus implemented controls.

## Automated gate

`scripts/validate_repository.py` fails closed on prohibited indicators and malformed files. The gate scans all files except Git metadata. It also verifies required public-governance files and relative links.

The detector is defense in depth, not proof of safety. A reviewer must confirm that architecture detail cannot be combined into a practical map of the private environment.

## History rule

Never initialize a public repository from a private repository's Git history. Build a fresh sanitized history. If a secret enters any public commit, remove access, rotate the credential, purge history, and assume the value was captured externally.

## Review checklist

1. Confirm the repository started from a clean public-only history.
2. Run repository validation and tests.
3. Review generated diagrams at rendered size.
4. Search commit history, not only the working tree.
5. Confirm only documentation/example domains and addresses are present.
6. Confirm no operational evidence or internal identifiers appear in filenames.
7. Confirm GitLab pipeline success at the exact commit.
8. Confirm GitHub readback after mirroring.
