# werk

A workout generator built as a **curated data library** plus two Claude Code skills. There is no algorithm or engine — Claude is the composer. You bring clean exercise data and named formats; Claude reads it and writes you a session tuned to the day's context (location, equipment, duration, who's in the room).

Focus areas: mobility, lower-body strength, and aggressive inline skating.

## Requirements

- [Claude Code](https://claude.com/claude-code) running in this repo. The skills live in `.claude/skills/` and load automatically.

## Quick start

```
/workout
```

Claude asks what it needs (location, equipment, duration, focus) and prints a session, saving a dated copy to `sessions/`.

```
/add-exercise <paste an article, a URL, or describe a movement>
```

Claude drafts a library entry, shows it to you, and only writes the file after you approve.

## Concepts (the nouns)

| Term | What it is |
|------|------------|
| **Session** | One generated workout. Stateless — made fresh each time, nothing remembered between runs. The output of `/workout`. |
| **Exercise** | A single movement, one markdown file in `exercises/`. Tagged with equipment, focus, movement pattern, level. **No sets/reps/load** — dosing is decided per session. |
| **Format** | A reusable session template (shape, timing, build rules), one file in `formats/`. A session can start from a format or be free-form. |
| **Location** | A named venue, one file in `locations/`, carrying its equipment list and notes on surface/space. Picking one pre-fills available equipment. |
| **Equipment** | What an exercise needs (dumbbell, band, skates, …). The one **hard filter** — Claude never programs gear you don't have. Everything else is judgment. |
| **Focus** | The quality an exercise trains (lower-body strength, hip mobility, balance, skating). Guides selection, not filtering. |

Full glossary: [CONTEXT.md](CONTEXT.md). Build plan and data model: [SPEC.md](SPEC.md). Controlled tag values: [vocabulary.md](vocabulary.md).

## Using `/workout`

Generates a session.

1. **Start point** — name a format (`Strength Circuit`, `Functional Mobility`) or just describe what you want ("45-min lower-body day for 8 people").
2. **Answer the prompts** — Claude asks for anything missing:
   - *Required:* location, equipment available, duration.
   - *Optional:* level (defaults to intermediate), focus/goal, group size (matters for station/circuit formats).
3. **Get the session** — Claude filters the library by your equipment, follows the format's build rules, and decides the dosing. The shape matches the format (e.g. a coach's run-sheet for a circuit). A dated file lands in `sessions/`.

**Flags:**
- `--terse` — collapse the output to a bare checklist for solo use, skipping the coaching run-sheet.

**Examples:**
```
/workout Strength Circuit
/workout functional mobility, 30 min, hips and ankles, at home, no equipment
/workout lower-body day at the Group Fitness Room, 6 people, 45 min --terse
```

## Using `/add-exercise`

Grows the exercise library from a source, behind a review gate.

1. **Input** — paste article text, give a URL, or describe a movement. Batch works (one article → many exercises).
2. **Dedup** — Claude scans `exercises/` for duplicates and offers merge / new / skip.
3. **Draft** — fills equipment, focus, movement pattern, level, progression/regression, and coaching cues; maps wording onto `vocabulary.md` and flags low-confidence fields or new tag candidates.
4. **Review** — Claude shows you the draft and takes edits. It never writes silently.
5. **Write** — approved exercises become `exercises/<kebab-name>.md`, with progression/regression refs cross-linked.

**Examples:**
```
/add-exercise https://example.com/article-on-cossack-squats
/add-exercise A horse stance squat: wide stance, toes out, sink to parallel and hold...
```

> Video ingestion is phase-2 and not yet wired up.

## Repository layout

```
werk/
├── CONTEXT.md       # glossary (the concepts)
├── SPEC.md          # build plan + data model
├── vocabulary.md    # controlled tag values
├── exercises/       # one .md per movement
├── formats/         # one .md per session template
├── locations/       # one .md per venue
├── sessions/        # generated outputs, dated
└── .claude/skills/  # /workout and /add-exercise
```

## Adding data by hand

You don't need `/add-exercise` — every file is plain markdown. Copy an existing `exercises/*.md` as a template, keep tag values inside `vocabulary.md`, and leave out dosing. New formats follow the skeleton in [SPEC.md](SPEC.md): **Shape · Timing · How to build it · Output · Notes**.
