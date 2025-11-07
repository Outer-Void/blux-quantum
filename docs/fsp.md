# bq fsp — Find Suspicious Patterns

**Purpose:** fast, local static scans for exfil, shell exec, secrets, and obfuscation.

```bash
bq fsp scan .
bq fsp scan . --staged -f jsonl
bq fsp scan . -f sarif -o out.sarif
```

Exit codes: 0 clean, 1 findings, 2 error / plugin missing.  
Default path: `~/.config/blux-lite-gold/logs/fsp.jsonl`

_(( • ))_
