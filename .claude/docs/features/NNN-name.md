# NNN Parry
Status: draft | planned | implemented | tuned

## Player-facing behaviour
Pressing LB during an enemy attack's parry window deflects it, staggers the boss
for N frames and opens a riposte.

## Acceptance criteria
- [ ] Parry succeeds only inside parry_window frames before active frames hit
- [ ] Failed parry has parry_recovery frames of vulnerability
- [ ] Unparryable attacks are flagged in their attack Resource and ignore parry
- [ ] Feel: successful parry is unmistakable (hitstop + flash + sound)

## New tunables
| name | unit | start | range |
| parry_window | frames | 6 | 3-10 |
| parry_recovery | frames | 20 | 10-30 |

## Must not change
Dodge timing, stamina costs of other actions.

## Open questions
- Does parry cost stamina?