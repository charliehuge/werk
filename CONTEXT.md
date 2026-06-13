# werk

A tool for generating workouts. A curated library of exercise data and named workout formats that Claude composes into a workout, driven by the context supplied at generation time.

## Language

**Workout**:
One generated workout instance — the output of the `/workout` skill. Generated fresh each time (stateless); nothing is remembered between workouts. Capitalized **Workout** = the instance/concept; lowercase "workout" = the broad domain the tool operates in.
_Avoid_: Session, routine

**Format**:
A named, reusable template describing the shape of a workout — its timing, structure, and how exercises are organized (e.g. stations, circuits, blocks). A workout may start from a format or be described free-form.
_Avoid_: Template, type, style

**Exercise**:
A single movement in the library, stored as a markdown file with frontmatter. Described by the **equipment** it requires, the **focus** (qualities) it trains, and an optional **requires** note for physical needs beyond equipment. Dosing (sets/reps/time/load) is never stored here — it is decided at the workout level.
_Avoid_: Movement, drill

**Equipment**:
What an exercise requires to perform (skates, bands, kettlebell, none). A hard, structured list. Skates are equipment, not a category — an on-skate drill is simply an exercise whose equipment includes skates. Filtered at generation against what the Location has on hand.

**Requires**:
An optional free-text note on an exercise for physical affordances beyond equipment — surface or space ("smooth flat surface", "overhead clearance"). Reasoned over as prose, not filtered as tags. A "setting" axis (gym/home/rink) was rejected as a lying proxy for equipment + surface + space.

**Focus**:
The quality an exercise trains (lower-body strength, hip mobility, balance, skating-specific). Drives selection, not filtering. An off-skate drill that trains skating ability has no skates in its equipment and so remains eligible for a gym workout.

**Progression / Regression**:
A harder / easier *movement variant* of an exercise, referencing another exercise by filename (e.g. Overhead Tricep Extension is a wrist-saving regression of Tricep Dip). Optional and multi-valued. A change in dosing — more/less weight, faster/slower tempo — is not a variant and does not belong here. Targets must be extant exercises.

**References (sources / videos)**:
Supplemental external material attached to an exercise — `sources` (URLs the exercise was drawn from) and `videos` (demo links, `{title, url}`). **For humans, never parsed**: a video is reference material, not a content source, and never builds an exercise on its own. Stored in frontmatter, rendered as links in the exercise's footer.

**Wiki**:
The repo is a navigable wiki — every file links to the related ones with GitHub-native relative markdown links (`[Name](slug.md)`, not `[[wikilinks]]`). Frontmatter slugs are the machine-readable source of truth; links are *generated* from them by `scripts/build-wiki.py` (exercise footers + the `exercises/README.md` index), so authors maintain frontmatter, not links. Workouts link their exercises back to the library. A future visualization layer reads the same frontmatter.

**Vocabulary**:
The controlled set of canonical tag values for the structured exercise fields (equipment, focus, movement pattern, level), kept in `vocabulary.md`. The structural twin of this glossary: `CONTEXT.md` governs concepts, `vocabulary.md` governs tag values. Both skills read it; ingest maps source synonyms onto canonical terms and prompts before adding a genuinely new value rather than silently creating variants.

**Location**:
A concrete named venue you define once and reuse: `{ name, equipment[], notes }`. E.g. "Group Fitness Room" with its dumbbell range, bands, boxes, and a `notes` line for surface/space ("sprung floor, low ceiling"). At generation, picking a Location pre-populates the available equipment (editable for the day) and supplies prose Claude reasons over. Stored as files, like Formats.
_Avoid_: Venue, place, gym

## Skills

**`/workout`**:
Generates a workout. Starts from a format or a free-form description, filters the exercise library by location and equipment, and composes the workout.

**`/add-exercise`**:
Takes a source (article, URL, description) and adds library exercises from it, behind a review gate.
