---
name: gdscript-conventions
description: GDScript style and Godot architecture conventions for this project.
user-invocable: false
paths: ["**/*.gd"]
---

- Static typing everywhere; no untyped var or untyped function signatures.
- One class per file, class_name for anything referenced from another scene.
- Signals named in past tense (hit_received, phase_changed).
- No get_node across scene roots; inject via @export or signals.
- Physics in _physics_process, input polling through the InputBuffer autoload only.