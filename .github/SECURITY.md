# Security Policy

Security is critical to the integrity of the SOFTCURSE system. We take vulnerabilities seriously and deploy patches aggressively.

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| v1.0.x  | ✅                  |
| < v1.0  | ❌                  |

## Reporting a Vulnerability

**DO NOT OPEN A PUBLIC GITHUB ISSUE for a security vulnerability.**

Please report any security concerns directly to the maintenance team using **GitHub Private Vulnerability Reporting** via the "Security" tab on the repository, or by emailing:
`softcursesystems@gmail.com`

**What to include in the report:**
- A detailed description of the vulnerability.
- Step-by-step instructions to reproduce the issue.
- Impact assessment (e.g., local arbitrary code execution, denial of service).
- Screenshots, crash logs, or proof-of-concept scripts.

## Response Timeline
- **Acknowledgement**: You will receive a response acknowledging the report within 48 hours.
- **Initial assessment**: We will complete an initial triaging and assessment within 7 days.
- **Patch or mitigation**: Verified vulnerabilities will be patched within 90 days.
- **Public disclosure**: We will publish a CVE and coordinate disclosure after the patch has been successfully distributed to the community.

## Security Advisories
All resolved vulnerabilities will be publicly disclosed as GitHub Security Advisories in this repository to inform end-users.

## Out of Scope
The following issues fall outside the scope of our security program:
- Denial of Service (DoS) attacks requiring massive local file sizes intentionally bypassing our 50MB safeguard.
- Social engineering attacks against maintainers or users.
- Flaws involving the underlying Chromium Edge/WebView2 rendering engine (these should be reported to Microsoft).

## Bug Bounty
At this time, SOFTCURSE/SYS does not operate a paid bug bounty program. We do, however, offer heartfelt gratitude and public CVE credits for responsible disclosures.

## Security Best Practices for Contributors
- Never commit hardcoded secrets, API keys, or personal tokens.
- Review any external HTML dependency additions; XSS vulnerabilities in the frontend UI are strictly to be avoided.
- Pin your dependency versions securely if making modifications to the PyInstaller configuration.
