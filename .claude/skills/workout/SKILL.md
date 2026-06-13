---
name: workout
description: Generate a workout Session from the werk exercise library — group class run-sheets, PT sessions, or terse self-workouts. Use when the user asks for a workout, a session, a class plan, or invokes /workout. Supports starting from a named format (formats/) or a free-form description; --terse collapses output to a bare checklist.
---

# /workout — Generate a Session

Composes one workout Session from the repo's data library. Stateless: everything comes from the context collected below. Domain language: `CONTEXT.md`. Tag values: `vocabulary.md`.

## Inputs

Parse whatever the user gave in the invocation first; **interactively prompt (AskUserQuestion) only for what's missing**.

Required:
- **Location** — a file in `locations/` (offer the list), or ad-hoc. Picking a Location pre-populates its equipment; ask "anything missing/extra today?" and let the user trim/add.
- **Duration** — total minutes.

Optional (don't block on these; infer or default):
- **Format** — a file in `formats/`, else free-form from the user's description.
- **Focus** — from `vocabulary.md` focus values or prose; formats may carry intrinsic focus.
- **Level** — default `intermediate`.
- **Group size** — only meaningful for station/circuit formats; adapt station count and pairing.
- **`--terse`** — collapse output to a bare checklist (self-use).

## Composition procedure

1. **Read the format file** (if any): structure, timing, selection rules, output shape. Free-form: propose a structure from the description, state it briefly, proceed.
2. **Resolve focus**: format's intrinsic focus first, session context narrows/overrides.
3. **Filter the library.** Scan frontmatter of every file in `exercises/`:
   - **Equipment is a hard filter**: exercise eligible iff its `equipment` list ⊆ available equipment. Never program around this.
   - **`requires` is soft**: reason its prose against the Location's `notes` (surface, space); exclude on contradiction (e.g. "smooth hard surface" vs grass).
4. **Select & arrange** per the format's rules (pattern balance, antagonist pairing, level spread). Selection is driven by focus; prefer exercises whose `level` fits, and use `progression`/`regression` fields to offer per-exercise scaling for mixed groups.
5. **Dose at session level** — sets/reps/work-rest/load live here, never in exercise files. Respect format defaults (e.g. Strength Circuit 1min/20s) unless context overrides.
6. **Sanity pass**: total time ≈ duration (warm-up + work + cooldown), no equipment violations, no two consecutive same-pattern stations where the format forbids it.

## Output

1. Render in the **format's Output shape** (run-sheet, sequence sheet, …). `--terse`: one-line-per-exercise checklist instead, keep dosing.
2. Write to `sessions/YYYY-MM-DD-<kebab-description>.md` (today's date; short description from focus/format). If the filename exists, append `-2`, `-3`, ….
3. Print the full session to the terminal too.

## Rules

- Use glossary terms (Session, Format, Location, Focus) exactly as defined in `CONTEXT.md`.
- If the library can't fill the plan (focus has too few eligible exercises), say so and name the gap — suggest `/add-exercise` rather than inventing non-library exercises. Inventing is allowed only if the user explicitly okays it; mark invented items *(not in library)*.
- Coaching cues in the output come from the exercise files' bodies — compress, don't rewrite.
