---
name: add-exercise
description: Add exercises to the werk library from a pasted article, URL, or freeform description — drafts frontmatter + coaching prose, dedups against existing exercises, and gates every write behind user review. Use when the user wants to add, ingest, or import an exercise (or batch of exercises) into exercises/, or invokes /add-exercise.
---

# /add-exercise — Grow the Exercise Library

Turns a source into one or more files in `exercises/`. Domain language: `CONTEXT.md`. Tag values: `vocabulary.md` — read it before drafting. **Never writes without explicit approval.**

## Input

- **Pasted text / prose description** — use as-is.
- **URL** — fetch it (WebFetch), extract exercise content.
- **Batch** — one source may yield many exercises (e.g. "5 best T-spine drills" article). Extract all; each goes through the same pipeline.
- **Video** — not supported (phase-2, see SPEC.md). Say so; offer to work from the user's own description or the video's text/transcript if they paste it.

## Pipeline (per exercise)

1. **Dedup.** Scan `exercises/*.md` frontmatter `name` + filenames for same or near-duplicate (synonym names, trivial variants). On hit, ask: **merge** (improve the existing file's body/tags), **new anyway** (it's genuinely distinct — say how), or **skip**.
2. **Draft.** Build the full file:
   ```yaml
   ---
   name: <Proper Name>
   equipment: [...]        # [] = bodyweight; vocabulary.md values only
   focus: [...]            # multi-valued
   movement_pattern: ...   # exactly one
   level: ...
   progression: [...]      # optional — filename refs, movement variants ONLY
   regression: [...]       # optional — never dosing changes (weight/tempo don't count)
   requires: ...           # optional prose — surface/space needs beyond equipment
   ---
   <2–4 short paragraphs: what it is, cues, common faults>
   ```
   - **Map synonyms onto vocabulary** ("DBs" → `dumbbell`). If the source needs a genuinely new vocab value, flag it — adding to `vocabulary.md` is its own approval, separate from the exercise.
   - **No dosing anywhere** — sets/reps/tempo/load from the source get dropped, not copied into the body.
   - `progression`/`regression` must point at extant files in `exercises/` — verify each ref exists. Within a batch, refs to siblings being added together are fine; cross-link both directions.
3. **Flag low confidence.** Mark any guessed field inline, e.g. `level: intermediate  # low confidence — source silent`. Don't hide uncertainty behind a clean draft.
4. **Review gate.** Show the complete draft(s). For batches, show all, then take edits per item. Ask: approve / edit / drop. **No write before approval.**
5. **Write.** `exercises/<kebab-name>.md` per approved exercise. Then verify: every `progression`/`regression` ref across the new files resolves to a file on disk. Report what was written and any vocabulary additions made.

## Rules

- Use glossary terms (Exercise, Equipment, Requires, Focus, Progression/Regression) per `CONTEXT.md`.
- Skates are equipment, not a category — an on-skate drill is `equipment: [skates, protective-gear]`, nothing more special than that.
- Body prose is coaching material: setup, cues, common faults. Rewrite source text into the library's voice (compare existing files); never paste walls of source text.
- When a source describes a variant chain ("can't do X? do Y"), capture it as `progression`/`regression` links, not as prose alternatives.
