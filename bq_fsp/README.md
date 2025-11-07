# bq-fsp — Find Suspicious Patterns

Fast regex/heuristic scanner for security patterns in code. Part of BLUX Quantum.

## Usage
```bash
bq fsp scan .                     # table view
bq fsp scan . --staged -f jsonl  # append to default JSONL log
bq fsp scan . -f sarif -o out.sarif
```

**Default log path:** `~/.config/blux-lite-gold/logs/fsp.jsonl`

Install plugin: `pip install bq-fsp`

_(( • ))_
