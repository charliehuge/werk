# Vocabulary

Canonical tag values for exercise frontmatter. Both `/workout` and `/add-exercise` read this file. Ingest maps source synonyms onto these terms ("DBs" → `dumbbell`) and prompts before adding a new value — never silently invents variants.

## equipment

Empty list = bodyweight.

- `dumbbell`
- `kettlebell`
- `band` — resistance band / mini band
- `box` — plyo box or sturdy bench-height surface
- `mat`
- `bench`
- `skates` — inline skates
- `protective-gear` — helmet, knee/wrist pads

## focus

- `lower-body-strength`
- `upper-body-strength`
- `core`
- `hip-mobility`
- `ankle-mobility`
- `t-spine-mobility`
- `balance`
- `skating` — trains skating ability, on- or off-skate
- `conditioning`

## movement_pattern

One value per exercise.

- `squat`
- `hinge`
- `lunge`
- `push`
- `pull`
- `carry`
- `rotation`
- `gait`
- `balance`

## level

- `beginner`
- `intermediate`
- `advanced`
