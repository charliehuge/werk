# werk — High-Level Spec

A tool for generating workout **Sessions** for group fitness classes, personal-training work, and the author's own training, with a focus on mobility, lower-body strength, and aggressive inline skating.

The repo is a **curated data library** (exercises, formats, locations) plus two Claude Code skills that compose and grow it. There is no generation engine — Claude is the composer. See [ADR-0001](docs/adr/0001-data-library-not-engine.md). Domain language is defined in [CONTEXT.md](CONTEXT.md); this spec is the build plan.

## Principles

- **Data + Claude, not an algorithm.** Value lives in clean data and precise vocabulary.
- **Stateless.** Each Session is generated fresh from supplied context. No client/person tracking in v1.
- **Equipment is a hard filter; everything else is judgment.** The one thing composition must get mechanically right is "don't program an exercise we can't equip."
- **Vocabulary discipline.** Structured tag values are controlled (`vocabulary.md`) so filters don't silently miss synonyms.

## Repository layout

```
werk/
├── CONTEXT.md            # glossary (concepts)
├── SPEC.md               # this file
├── vocabulary.md         # controlled tag values (equipment, focus, movement_pattern, level)
├── exercises/            # one .md per exercise — flat, kebab-case
├── formats/              # one .md per format — prose skeleton
├── locations/            # one .md per venue — {name, equipment[], notes}
├── sessions/             # generated outputs, dated
├── docs/adr/             # architecture decision records
└── .claude/skills/
    ├── workout/          # /workout
    └── add-exercise/     # /add-exercise
```

Flat directories throughout. `focus` is multi-valued, so folders would force a false single home; Claude scans frontmatter across the flat dir. Add an index only if scanning gets slow.

## Data model

### Exercise (`exercises/*.md`)

Markdown with YAML frontmatter; body is coaching prose. **No dosing** — sets/reps/time/load are decided at the Session level.

```yaml
---
name: Goblet Squat
equipment: [kettlebell]            # [] = bodyweight. Hard filter. Skates are equipment.
focus: [lower-body-strength, hip-mobility]
movement_pattern: squat            # squat/hinge/push/pull/carry/rotation/gait/balance
level: beginner                    # beginner/intermediate/advanced
progression: [front-squat]         # optional, multi — filename refs to extant exercises
regression: [box-squat]            # optional, multi
requires: smooth flat surface      # optional free prose — affordances beyond equipment
---

Coaching cues, setup, common faults, breathing…
```

- `equipment`, `focus`, `movement_pattern`, `level` draw from `vocabulary.md`.
- `progression`/`regression` are **movement variants only** (e.g. Overhead Tricep Extension regresses Tricep Dip), never dosing changes; targets must be existing exercise files.
- `requires` captures surface/space needs Claude reasons over as prose (no `setting` axis — it was rejected as a lying proxy for equipment + surface + space).

### Format (`formats/*.md`)

Prose with a consistent skeleton. Carries **structure always** and **intrinsic selection rules when applicable**, and defines the Session's output shape.

Skeleton headings: **Shape** · **Timing** · **How to build it** (selection/balance rules) · **Output** · **Notes**.

- *Strength Circuit* — stations/rounds/work-rest structure; focus inherited from context.
- *Functional Mobility* — implies focus = mobility, controlled tempo, no loading to failure.

A Session may also be **free-form** (no format) — Claude proposes structure from the description.

### Location (`locations/*.md`)

A concrete named venue, defined once and reused.

```yaml
---
name: Group Fitness Room
equipment: [dumbbell, band, box, mat]
notes: sprung floor, low ceiling, ~400 sq ft
---
```

At generation, picking a Location pre-populates available equipment (editable for the day) and supplies prose Claude reasons over for surface/space.

### Vocabulary (`vocabulary.md`)

Canonical values for `equipment`, `focus`, `movement_pattern`, `level`. Both skills read it. Ingest maps source synonyms (e.g. "DBs" → `dumbbell`) onto canonical terms and prompts before adding a genuinely new value.

### Session (`sessions/YYYY-MM-DD-description.md`)

Saved generated output (also printed to terminal). Markdown, printable/phone-friendly. A saved artifact, not tracked state.

## Skill: `/workout`

Generates a Session.

1. **Start point** — a Format, or a free-form description.
2. **Collect context** — interactively prompt for anything missing:
   - Required: location, equipment available, duration.
   - Optional: level (default intermediate), focus/goal, group size (only meaningful for station/circuit formats).
3. **Resolve** — Format sets structure + intrinsic focus → context overrides/adds focus → filter exercises by `equipment ∩ requires` (Location-derived) → Claude composes respecting the Format's selection/balance rules and decides dosing.
4. **Output** — shape defined by the Format; `--terse` collapses any Session to a bare checklist for self-use. Write a dated file to `sessions/` and print to terminal.

## Skill: `/add-exercise`

Grows the library from sources.

1. **Input** — pasted text, URL, or freeform description. Supports **batch** (one article → many exercises).
2. **Dedup** — scan `exercises/` for same/near-duplicate; offer merge / new / skip.
3. **Draft** — fill `equipment`, `focus`, `movement_pattern`, `level`, `progression`/`regression`, cues; map tags onto `vocabulary.md` and flag low-confidence fields and new vocab candidates.
4. **Review gate** — show the draft, take edits/approval. Never silent-writes.
5. **Write** — emit `exercises/<kebab-name>.md` per approved exercise. Within a batch, cross-link progression/regression refs.

**Video is phase-2.** Claude has no native video modality; the documented path is a preprocessing step inside this skill — `ffmpeg` keyframe extraction + audio transcript (whisper) → frames + text feed the same draft→review→write flow.

## Build order (suggested)

1. `vocabulary.md` — seed equipment/focus/pattern/level.
2. Two `formats/` files — Strength Circuit, Functional Mobility.
3. A handful of `exercises/` and one `locations/` file — enough to exercise the flow.
4. `/workout` skill against that seed data.
5. `/add-exercise` skill to scale the library.

## Out of scope (v1)

Client/person tracking and progression-over-time · a deterministic generation engine · video ingestion · any non–Claude-Code surface (web/phone/print app).
