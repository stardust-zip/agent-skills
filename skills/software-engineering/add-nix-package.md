---
name: add-nix-package
description: How to correctly install a new tool or package on this system.
---

## System Rules

This system does NOT use `apt`, `brew`, or global `npm install`. Everything is managed declaratively via Nix and Home-Manager.

## The Procedure

If the user asks to "install [X]" or "add [X] to my system":

1. Check if the package exists in Nixpkgs.
2. In the home-manager repo (see its `AGENTS.md`): a package that needs no configuration goes in the list in `packages.nix`; one that is configured gets its own module, `programs/<ai|cli|desktop|editors>/<name>.nix`, imported in `home.nix` (and in `home-phone.nix` too if it is a CLI tool that works on the phone).
3. Never attempt to run `sudo apt install` or modify global system state directly.
4. After updating the `.nix` file, remind the user to run their Home-Manager switch command.
