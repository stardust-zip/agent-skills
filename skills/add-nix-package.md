---
name: add-nix-package
description: How to correctly install a new tool or package on this system.
---

## System Rules

This system does NOT use `apt`, `brew`, or global `npm install`. Everything is managed declaratively via Nix and Home-Manager.

## The Procedure

If the user asks to "install [X]" or "add [X] to my system":

1. Check if the package exists in Nixpkgs.
2. If it is a CLI tool or application, add it to the `home.packages` list in the appropriate `.nix` file within the `programs/` directory.
3. Never attempt to run `sudo apt install` or modify global system state directly.
4. After updating the `.nix` file, remind the user to run their Home-Manager switch command.
