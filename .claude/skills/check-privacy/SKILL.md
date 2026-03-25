---
name: check-privacy
description: Scan repository for security and privacy risks before pushing to GitHub — API keys, credentials, tokens, personal information, hardcoded paths, and sensitive data
user-invocable: true
disable-model-invocation: false
allowed-tools: Read, Grep, Glob, Bash, Agent
---

# Check Privacy — Pre-Push Security & Privacy Scan

Scan all tracked and staged files in this repository for security and privacy risks before pushing to GitHub. Report findings grouped by severity.

## What to scan for

### Critical (must fix before push)
- **API keys & tokens**: OpenAI, Anthropic, AWS, GCP, Azure, Slack, GitHub, Zotero tokens, any string matching common key patterns (sk-..., ghp_..., xoxb-..., AKIA..., etc.)
- **Passwords & secrets**: hardcoded passwords, database connection strings with credentials, private keys (RSA, SSH, PGP), certificates
- **Environment variable values**: .env files or inline env values that contain real secrets
- **OAuth tokens, JWTs, session tokens**
- **Claude Code safety overrides**: Any `.claude/settings.json` (the committed, non-local variant) that contains permissive permission grants like `Bash(*)`, `Write(*)`, `Edit(*)`, `mcp__*`, or other wildcard allow rules. These would give students who clone the repo wide-open permissions with no safety prompts. The `.claude/settings.local.json` is safe IF it is in `.gitignore` — but `.claude/settings.json` is committed by default and must not contain relaxed permissions.

### High (strongly recommend fixing)
- **Personal information**: email addresses, phone numbers, physical addresses, student IDs, patient IDs, IP addresses
- **Hardcoded absolute paths** containing usernames (e.g., `/Users/mth/`, `/home/username/`)
- **Database dumps or exports** accidentally included
- **Large binary files** that shouldn't be in version control (>.5 MB)

### Medium (review recommended)
- **Internal URLs**: localhost endpoints, internal network addresses, staging/dev server URLs
- **Commented-out credentials** or TODOs referencing secrets
- **Slack webhook URLs, Notion API links**
- **Hardcoded usernames or server names**

## Procedure

1. **Get the file list**: Use `git ls-files` to get all tracked files, plus `git diff --cached --name-only` for staged but uncommitted files. Exclude binary files and common non-text formats (.png, .jpg, .tiff, .pdf, .pkl, .parquet, .h5).

2. **Pattern scan**: Search all text files for the patterns listed above using Grep. Use regex patterns such as:
   - `(?i)(api[_-]?key|secret[_-]?key|access[_-]?token|auth[_-]?token|password|passwd|credential)\s*[=:]\s*['"]?\w`
   - `sk-[a-zA-Z0-9]{20,}`
   - `ghp_[a-zA-Z0-9]{36}`
   - `xox[bprs]-[a-zA-Z0-9-]+`
   - `AKIA[0-9A-Z]{16}`
   - `-----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----`
   - Email regex: `[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}`
   - Absolute home paths: `/Users/\w+/|/home/\w+/`
   - IP addresses: `\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b`

3. **Check .gitignore coverage**: Verify that `.env`, `*.pem`, `*.key`, `credentials.*`, `.claude/settings.local.json`, and common secret file patterns are in `.gitignore`. Flag any that are missing.

4. **Claude Code settings audit**:
   - Check if `.claude/settings.json` (the committed variant) exists and is tracked. If it exists, read it and flag any permissive `allow` rules (wildcards like `Bash(*)`, `Write(*)`, `mcp__*`). These override safety prompts for anyone who clones the repo.
   - Verify `.claude/settings.local.json` is in `.gitignore` and NOT tracked by git. If it IS tracked, this is **critical** — it likely contains personal API keys and relaxed permissions.
   - Check any env vars defined in settings files for real secrets (API keys, tokens).

5. **Large file check**: Use `git ls-files` piped through file size check to find any files over 500KB that are tracked.

6. **Review the SKILL.md itself and other skill/config files** for embedded secrets.

## Output format

Present a clear report:

```
## Privacy & Security Scan Results

### Critical 🔴
- [file:line] Description of finding

### High 🟠
- [file:line] Description of finding

### Medium 🟡
- [file:line] Description of finding

### .gitignore Coverage
- ✅ Pattern covered
- ❌ Pattern missing — recommend adding

### Summary
X critical, Y high, Z medium findings
Recommendation: SAFE TO PUSH / FIX BEFORE PUSHING
```

If there are **zero critical findings**, state "SAFE TO PUSH" but still list any high/medium items for awareness. If there are **any critical findings**, state "FIX BEFORE PUSHING" and list exactly what needs to change.

## Exclusions
- Ignore patterns inside this SKILL.md file itself (these are example patterns, not real secrets)
- Ignore `.claude/` config files that are already in `.gitignore`
- Ignore test fixtures or mock data that are clearly fake (e.g., `test_api_key = "fake-key-for-testing"`)
- Use judgment: a regex pattern in source code is not a secret; an actual key value is
