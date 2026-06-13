# werk — High-Level Spec

A tool for generating **Workouts** for group fitness classes, personal-training work, and the author's own training, with a focus on mobility, lower-body strength, and aggressive inline skating.

The repo is a **curated data library** (exercises, formats, locations) plus two Claude Code skills that compose and grow it. There is no generation engine — Claude is the composer. See [ADR-0001](docs/adr/0001-data-library-not-engine.md). Domain language is defined in [CONTEXT.md](CONTEXT.md); this spec is the build plan.

## Principles

- **Data + Claude, not an algorithm.** Value lives in clean data and precise vocabulary.
- **Stateless.** Each Workout is generated fresh from supplied context. No client/person tracking in v1.
- **Equipment is a hard filter; everything else is judgment.** The one thing composition must get mechanically right is "don't program an exercise we can't equip."
- **Vocabulary discipline.** Structured tag values are controlled (`vocabulary.md`) so filters don't silently miss synonyms.

## Repository layout

```
werk/
├── CONTEXT.md            # glossary (concepts)
├── SPEC.md               # this file
├── vocabulary.md         # controlled tag values (equipment, focus, movement_pattern, level)
├── exercises/            # one .md per exercise — flat, kebab-case + README.md index
├── formats/              # one .md per format — prose skeleton
├── locations/            # one .md per venue — {name, equipment[], notes}
├── workouts/             # generated outputs, dated
├── scripts/build-wiki.py # regenerates exercise footers + index from frontmatter
├── docs/adr/             # architecture decision records
└── .claude/skills/
    ├── workout/          # /workout
    └── add-exercise/     # /add-exercise
```

Flat directories throughout. `focus` is multi-valued, so folders would force a false single home; Claude scans frontmatter across the flat dir. Add an index only if scanning gets slow.

## Data model

### Exercise (`exercises/*.md`)

Markdown with YAML frontmatter; body is coaching prose. **No dosing** — sets/reps/time/load are decided at the Workout level.

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
sources: [https://…]               # optional — URL(s) the exercise was drawn from
videos:                            # optional — supplemental demos for humans, never parsed
  - title: Squat University demo
    url: https://youtu.be/…
---

Coaching cues, setup, common faults, breathing…

---

<!-- wiki-footer -->
Generated link footer (Trains / Progressions & regressions / References).
```

- `equipment`, `focus`, `movement_pattern`, `level` draw from `vocabulary.md`.
- `progression`/`regression` are **movement variants only** (e.g. Overhead Tricep Extension regresses Tricep Dip), never dosing changes; targets must be existing exercise files.
- `requires` captures surface/space needs Claude reasons over as prose (no `setting` axis — it was rejected as a lying proxy for equipment + surface + space).
- `sources` and `videos` are **reference material for humans**, not parsed. A video link is supplemental only — it never builds an exercise.

### Wiki linking

The repo is a **navigable wiki**: every markdown file links to the related ones, GitHub-native (relative `[Name](slug.md)` links — no `[[wikilinks]]`). Frontmatter slugs stay the machine-readable source of truth; links are rendered from them.

- **Exercise footer** — below a `<!-- wiki-footer -->` sentinel, each file carries generated links: **Trains** (focus/equipment/pattern/level → `vocabulary.md` sections), **Progressions & regressions** (→ exercise files), **References** (`sources`/`videos`). Authors write only frontmatter + prose *above* the sentinel.
- **Index** — `exercises/README.md` lists every exercise grouped by focus, each linked.
- **Workouts** — generated workouts link each exercise name to its library file.
- **Generator** — `scripts/build-wiki.py` is the single authority for footers + index. It reads frontmatter, regenerates everything below the sentinel, rebuilds the index, and flags unresolved `progression`/`regression` refs. Idempotent; safe to re-run. Hand-maintained backlinks are out of scope — a future visualization layer derives the reverse graph from the same frontmatter.

### Format (`formats/*.md`)

Prose with a consistent skeleton. Carries **structure always** and **intrinsic selection rules when applicable**, and defines the Workout's output shape.

Skeleton headings: **Shape** · **Timing** · **How to build it** (selection/balance rules) · **Output** · **Notes**.

- *Strength Circuit* — stations/rounds/work-rest structure; focus inherited from context.
- *Functional Mobility* — implies focus = mobility, controlled tempo, no loading to failure.

A Workout may also be **free-form** (no format) — Claude proposes structure from the description.

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

### Workout (`workouts/YYYY-MM-DD-description.md`)

Saved generated output (also printed to terminal). Markdown, printable/phone-friendly. A saved artifact, not tracked state.

## Skill: `/workout`

Generates a Workout.

1. **Start point** — a Format, or a free-form description.
2. **Collect context** — interactively prompt for anything missing:
   - Required: location, equipment available, duration.
   - Optional: level (default intermediate), focus/goal, group size (only meaningful for station/circuit formats).
3. **Resolve** — Format sets structure + intrinsic focus → context overrides/adds focus → filter exercises by `equipment ∩ requires` (Location-derived) → Claude composes respecting the Format's selection/balance rules and decides dosing.
4. **Output** — shape defined by the Format; `--terse` collapses any Workout to a bare checklist for self-use. Write a dated file to `workouts/` and print to terminal.

## Skill: `/add-exercise`

Grows the library from sources.

1. **Input** — pasted text, URL, or freeform description. Supports **batch** (one article → many exercises).
2. **Dedup** — scan `exercises/` for same/near-duplicate; offer merge / new / skip.
3. **Draft** — fill `equipment`, `focus`, `movement_pattern`, `level`, `progression`/`regression`, cues; map tags onto `vocabulary.md` and flag low-confidence fields and new vocab candidates.
4. **Review gate** — show the draft, take edits/approval. Never silent-writes.
5. **Write** — emit `exercises/<kebab-name>.md` (frontmatter + prose) per approved exercise, then run `scripts/build-wiki.py` to render footers and rebuild the index. Within a batch, cross-link progression/regression refs.

**Video is supplemental, not a source.** Claude has no native video modality and does not parse video. A video link is captured as a `videos:` reference attached to an exercise — extra material for humans. Building an exercise still needs text (a description, transcript, or article); a video alone prompts the user for that text, then the link rides along as a reference.

## Build order (suggested)

1. `vocabulary.md` — seed equipment/focus/pattern/level.
2. Two `formats/` files — Strength Circuit, Functional Mobility.
3. A handful of `exercises/` and one `locations/` file — enough to exercise the flow.
4. `/workout` skill against that seed data.
5. `/add-exercise` skill to scale the library.

## Out of scope (v1)

Client/person tracking and progression-over-time · a deterministic generation engine · video *parsing* (videos are supplemental links only) · hand-maintained backlinks (a future viz derives the reverse graph) · any non–Claude-Code surface (web/phone/print app).
