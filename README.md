# Agent Skill Sync (`agent-skill-sync`)

A canonical skill symlink manager for Google Antigravity and AI coding assistants.

## Overview

`agent-skill-sync` scans canonical skill source repositories under `~/code/github/` and maintains clean, single-source-of-truth symlinks across:
1. `~/.agents/skills/`
2. `~/.gemini/skills/`

## Quick Start

### Audit Skill Symlinks
```bash
python3 skills/skill-sync/scripts/sync_skills.py
```

### Auto-Repair & Fix Symlinks
```bash
python3 skills/skill-sync/scripts/sync_skills.py --fix
```

## License

Apache License 2.0. See [LICENSE](LICENSE) for details.
