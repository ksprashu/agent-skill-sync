---
name: skill-sync
description: Scans canonical skill source repositories in ~/code/github and manages symlinks across ~/.agents/skills and ~/.gemini/skills to maintain single source-of-truth skill directory synchronization.
---

# Skill Sync - Canonical Skill Symlink Manager

Use this skill whenever you need to verify, audit, repair, or synchronize custom AI agent skills across user skill directories.

## Overview
Canonical skill sources are maintained in individual git repositories under `~/code/github/skills-*`, `~/code/github/agent-*`, or `~/code/github/gcx-*`. 
To ensure agents in Antigravity and AI coding environments have access to all skills without duplicating files, `skill-sync` maintains symlinks in:
1. `~/.agents/skills/`
2. `~/.gemini/skills/`

## Usage Instructions

### 1. Audit Skill Symlinks
Run the sync audit script to inspect missing or broken symlinks:
```bash
python3 /Users/ksprashanth/code/github/agent-skill-sync/skills/skill-sync/scripts/sync_skills.py
```

### 2. Automatically Repair & Synchronize Symlinks
To automatically create missing symlinks or fix broken target paths:
```bash
python3 /Users/ksprashanth/code/github/agent-skill-sync/skills/skill-sync/scripts/sync_skills.py --fix
```

## Best Practices
- When adding a new custom skill, place its canonical source repository in `~/code/github/skills-<skill-name>/skills/<skill-name>` (or `~/code/github/agent-<skill-name>`) and run `python3 .../sync_skills.py --fix`.
- Ensure each canonical skill includes a valid `SKILL.md` file with standard YAML frontmatter (`name`, `description`).
