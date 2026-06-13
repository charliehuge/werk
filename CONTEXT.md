# werk

A tool for generating workouts. A curated library of exercise data and named workout formats that Claude composes into a workout, driven by the context supplied at generation time.

## Language

**Session**:
One generated workout instance — the output of the `/workout` skill. Generated fresh each time (stateless); nothing is remembered between sessions.
_Avoid_: Workout (ambiguous — refers to the whole domain), routine

**Format**:
A named, reusable template describing the shape of a session — its timing, structure, and how exercises are organized (e.g. stations, circuits, blocks). A session may start from a format or be described free-form.
_Avoid_: Template, type, style

**Exercise**:
A single movement in the library, stored as a markdown file with frontmatter. Described by the **equipment** it requires, the **focus** (qualities) it trains, and an optional **requires** note for physical needs beyond equipment. Dosing (sets/reps/time/load) is never stored here — it is decided at the session level.
_Avoid_: Movement, drill

**Equipment**:
What an exercise requires to perform (skates, bands, kettlebell, none). A hard, structured list. Skates are equipment, not a category — an on-skate drill is simply an exercise whose equipment includes skates. Filtered at generation against what the Location has on hand.

**Requires**:
An optional free-text note on an exercise for physical affordances beyond equipment — surface or space ("smooth flat surface", "overhead clearance"). Reasoned over as prose, not filtered as tags. A "setting" axis (gym/home/rink) was rejected as a lying proxy for equipment + surface + space.

**Focus**:
The quality an exercise trains (lower-body strength, hip mobility, balance, skating-specific). Drives selection, not filtering. An off-skate drill that trains skating ability has no skates in its equipment and so remains eligible for a gym session.

**Progression / Regression**:
A harder / easier *movement variant* of an exercise, referencing another exercise by filename (e.g. Overhead Tricep Extension is a wrist-saving regression of Tricep Dip). Optional and multi-valued. A change in dosing — more/less weight, faster/slower tempo — is not a variant and does not belong here. Targets must be extant exercises.

**Vocabulary**:
The controlled set of canonical tag values for the structured exercise fields (equipment, focus, movement pattern, level), kept in `vocabulary.md`. The structural twin of this glossary: `CONTEXT.md` governs concepts, `vocabulary.md` governs tag values. Both skills read it; ingest maps source synonyms onto canonical terms and prompts before adding a genuinely new value rather than silently creating variants.

**Location**:
A concrete named venue you define once and reuse: `{ name, equipment[], notes }`. E.g. "Group Fitness Room" with its dumbbell range, bands, boxes, and a `notes` line for surface/space ("sprung floor, low ceiling"). At generation, picking a Location pre-populates the available equipment (editable for the day) and supplies prose Claude reasons over. Stored as files, like Formats.
_Avoid_: Venue, place, gym

## Skills

**`/workout`**:
Generates a session. Starts from a format or a free-form description, filters the exercise library by location and equipment, and composes the session.

**`/ingest-exercise`**:
Takes a source (video, article, etc.) and generates a library exercise from it.
