# [Game name]
Godot 4.7.x, GDScript, statically typed. 2D. Target: 60 fps, Xbox controller first.

## Source of truth
- Design: docs/design/one-pager.md, docs/design/tuning.md
- Features: docs/features/NNN-*.md (implement only what the spec says)

## Architecture rules
- Composition: Health, Hitbox, Hurtbox, StaminaPool, StateMachine are reusable nodes
- One script per state under scenes/<entity>/states/
- Every tunable is an @export on a Tuning resource in data/, named as in tuning.md
- Timing values in frames @60 unless the name ends in _ms
- Signals for events, direct calls for commands; no get_node across scene roots
- Game logic in pure functions where possible; tests in test/unit/
- Do not edit .tscn files larger than ~100 lines; describe the change instead

## Definition of done
- gdlint and gdformat clean, headless import clean, all tests green
- tuning.md updated for any new value
- Short note: what to playtest, what to watch for

## Commands
- Tests: godot --headless -s addons/gut/gut_cmdln.gd -gdir=res://test -ginclude_subdirs -gexit
- Import check: godot --headless --path . --import
- Syntax check of one script: godot --headless --path . --check-only -s res://path/to/script.gd
- Smoke run: godot --headless --path . --quit-after 120