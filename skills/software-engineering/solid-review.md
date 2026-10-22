---
name: solid-review
description: Review an existing file or codebase for architectural flaws and maintainability.
---

## The Rubric

When reviewing code, aggressively look for the following violations:

- **God Objects/Functions:** Is there a function longer than 50 lines? Does a class handle both UI rendering and data fetching?
- **Hidden Dependencies:** Are external libraries or database connections instantiated deep inside business logic instead of being passed in?
- **Mutation:** Are there unnecessary `let` variables or arrays being mutated in place instead of returning new copies?
- **Magic Strings/Numbers:** Are there hardcoded values that should be extracted to constants or configuration files?

## Output Format

1. **The Flaw:** Quote the exact lines of code that violate the principle.
2. **The Principle:** Name the specific SOLID or declarative principle being violated.
3. **The Fix:** Provide the refactored code block.
