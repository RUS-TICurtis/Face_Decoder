---
name: document-changes
description: "Documents every codebase change (minor, major, etc.) into the docs/ folder."
---

# Document Changes

## Overview
This skill instructs the agent to systematically document every change it makes to the codebase. It ensures a high standard of maintainability by keeping a persistent, human-readable record of modifications.

## When to Use
- Invoke this skill at the end of any coding session.
- Use it whenever you have completed modifications to the codebase, no matter how minor.

## Instructions
1. **Ensure the `docs/` directory exists** in the root of the workspace. If it does not exist, create it.
2. **Locate or create a changelog document** (e.g., `docs/CHANGELOG.md` or `docs/CHANGES.md`).
3. **Record the changes**:
   - Add a new entry with the current date/timestamp.
   - Summarize the high-level goal of the changes.
   - List every file modified, created, or deleted.
   - Describe both major architectural shifts and minor bug fixes.
   - Include any reasoning or context that a future developer or agent might need to know.
4. **Persist the file** by writing the updates to the file system.
