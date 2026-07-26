#!/usr/bin/env python3
"""
Skill Sync - Canonical Skill Symlink Manager
Scans canonical skill source repositories in ~/code/github and manages symlinks
across ~/.agents/skills and ~/.gemini/skills.
"""

import os
import sys
import argparse

GITHUB_DIR = os.path.expanduser('~/code/github')
AGENTS_SKILLS_DIR = os.path.expanduser('~/.agents/skills')
GEMINI_SKILLS_DIR = os.path.expanduser('~/.gemini/skills')
CLAUDE_SKILLS_DIR = os.path.expanduser('~/.claude/skills')


def discover_canonical_skills():
    """Find all canonical skills in ~/code/github."""
    skills = {}
    if not os.path.exists(GITHUB_DIR):
        return skills

    for repo in os.listdir(GITHUB_DIR):
        repo_path = os.path.join(GITHUB_DIR, repo)
        if not os.path.isdir(repo_path):
            continue

        # Check for skills/<skill-name>/SKILL.md
        inner_skills = os.path.join(repo_path, 'skills')
        if os.path.isdir(inner_skills):
            for sk in os.listdir(inner_skills):
                sk_path = os.path.join(inner_skills, sk)
                if os.path.isdir(sk_path) and os.path.exists(os.path.join(sk_path, 'SKILL.md')):
                    skills[sk] = sk_path
        
        # Check direct SKILL.md in repo root
        elif os.path.exists(os.path.join(repo_path, 'SKILL.md')):
            sk_name = repo.replace('skills-', '').replace('gcx-', '').replace('agent-', '')
            skills[sk_name] = repo_path

    return skills


def clean_orphan_symlinks(skills_dir, canonical_skills, fix=False):
    """Remove symlinks pointing to non-existent skills or target paths."""
    if not os.path.exists(skills_dir):
        return

    for item in os.listdir(skills_dir):
        item_path = os.path.join(skills_dir, item)
        if os.path.islink(item_path):
            target_exists = os.path.exists(item_path)
            is_canonical = item in canonical_skills
            if not target_exists or not is_canonical:
                print(f"  [ORPHAN/BROKEN LINK] {item} in {skills_dir}")
                if fix:
                    os.unlink(item_path)
                    print(f"    -> Removed orphan link: {item_path}")


def audit_and_sync(fix=False):
    canonical_skills = discover_canonical_skills()
    print(f"Discovered {len(canonical_skills)} canonical skills in {GITHUB_DIR}:")
    for name, path in sorted(canonical_skills.items()):
        print(f"  - {name}: {path}")

    os.makedirs(AGENTS_SKILLS_DIR, exist_ok=True)
    os.makedirs(GEMINI_SKILLS_DIR, exist_ok=True)
    os.makedirs(CLAUDE_SKILLS_DIR, exist_ok=True)

    print("\n--- Auditing ~/.agents/skills ---")
    clean_orphan_symlinks(AGENTS_SKILLS_DIR, canonical_skills, fix=fix)
    for name, src_path in sorted(canonical_skills.items()):
        target_link = os.path.join(AGENTS_SKILLS_DIR, name)
        if not os.path.exists(target_link) and not os.path.islink(target_link):
            print(f"  [MISSING] {name} in ~/.agents/skills")
            if fix:
                os.symlink(src_path, target_link)
                print(f"    -> Linked {target_link} -> {src_path}")
        elif os.path.islink(target_link):
            link_dst = os.readlink(target_link)
            if not os.path.exists(target_link):
                print(f"  [BROKEN LINK] {name} in ~/.agents/skills ({link_dst})")
                if fix:
                    os.unlink(target_link)
                    os.symlink(src_path, target_link)
                    print(f"    -> Repaired link to {src_path}")
            else:
                print(f"  [OK] {name} -> {link_dst}")

    print("\n--- Auditing ~/.gemini/skills ---")
    clean_orphan_symlinks(GEMINI_SKILLS_DIR, canonical_skills, fix=fix)
    for name, src_path in sorted(canonical_skills.items()):
        # Prefer linking to ~/.agents/skills/<name> if it exists, otherwise directly to source
        agent_link = os.path.join(AGENTS_SKILLS_DIR, name)
        target_path = agent_link if os.path.exists(agent_link) else src_path
        
        gemini_link = os.path.join(GEMINI_SKILLS_DIR, name)
        if not os.path.exists(gemini_link) and not os.path.islink(gemini_link):
            print(f"  [MISSING] {name} in ~/.gemini/skills")
            if fix:
                os.symlink(target_path, gemini_link)
                print(f"    -> Linked {gemini_link} -> {target_path}")
        elif os.path.islink(gemini_link):
            link_dst = os.readlink(gemini_link)
            if not os.path.exists(gemini_link):
                print(f"  [BROKEN LINK] {name} in ~/.gemini/skills ({link_dst})")
                if fix:
                    os.unlink(gemini_link)
                    os.symlink(target_path, gemini_link)
                    print(f"    -> Repaired link to {target_path}")
            else:
                print(f"  [OK] {name} -> {link_dst}")

    print("\n--- Auditing ~/.claude/skills ---")
    clean_orphan_symlinks(CLAUDE_SKILLS_DIR, canonical_skills, fix=fix)
    for name, src_path in sorted(canonical_skills.items()):
        agent_link = os.path.join(AGENTS_SKILLS_DIR, name)
        target_path = agent_link if os.path.exists(agent_link) else src_path
        
        claude_link = os.path.join(CLAUDE_SKILLS_DIR, name)
        if not os.path.exists(claude_link) and not os.path.islink(claude_link):
            print(f"  [MISSING] {name} in ~/.claude/skills")
            if fix:
                os.symlink(target_path, claude_link)
                print(f"    -> Linked {claude_link} -> {target_path}")
        elif os.path.islink(claude_link):
            link_dst = os.readlink(claude_link)
            if not os.path.exists(claude_link):
                print(f"  [BROKEN LINK] {name} in ~/.claude/skills ({link_dst})")
                if fix:
                    os.unlink(claude_link)
                    os.symlink(target_path, claude_link)
                    print(f"    -> Repaired link to {target_path}")
            else:
                print(f"  [OK] {name} -> {link_dst}")


def main():
    parser = argparse.ArgumentParser(description="Skill Sync CLI")
    parser.add_argument('--fix', action='store_true', help="Automatically create/repair missing symlinks")
    args = parser.parse_args()
    audit_and_sync(fix=args.fix)


if __name__ == '__main__':
    main()
