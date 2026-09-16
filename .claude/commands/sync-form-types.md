---
description: Regenerate app-behavior.md's Form Types table from the ontology (the .ttl files are authoritative), and write descriptions for any newly-added form type
---

Reconcile the **Form Types** table in `app-behavior.md`'s [Adding a Tool](../../app-behavior.md#adding-a-tool) section against the ontology. The table lists every SHACL shape the app's **Add Tool** dialog offers as a form's template — the value stamped onto the new graph as its `cell:shape`.

**The `.ttl` files are authoritative.** Where the table and the ontology disagree, the table is wrong. This is a one-directional sync: ontology → `app-behavior.md`.

`helpers/form-types.py` does the mechanical half. It owns the table's **row set**, its **shape CURIE** column and its **Declared by** column, reading them from `helpers/validate.py`'s `SHAPE_TO_FILE` registry and from every `cell:formShape`/`cell:memberShape` in `cat-templates.ttl` and `category-ext/*.ttl`. It does **not** write the display name or the description — those are the app's own UI wording, and your job here.

## Method

1. Run `python3 helpers/form-types.py --check` from the repo root.
   - **Exit 0, no output but the match line** → nothing to do. Say so and stop; do not edit the file.
   - **"Shapes that are neither a registered form type nor a component of one"** → a shape was added to a `**/shacl/*.ttl` file and never classified. Resolve this *first*, before touching the table: read the shape and decide whether a user could sensibly add it as a form. If yes, register it in `helpers/validate.py`'s `SHAPE_TO_FILE` (and `SHAPE_NS`/`PREFIX_TO_FILES` too, if its shapes file is new — that registry is what the validator resolves a `cell:shape` value against, so the gap is a validation gap as much as a docs one). If no, it belongs under the script's `INFRA_FILES` rule or is a component shape already; say which and leave it out.
   - **A unified diff of the table** → go on to step 2.
2. Run `python3 helpers/form-types.py --write`. Surviving rows keep their order, name and description; the shape and Declared by columns are rewritten; a shape that left the registry loses its row; a new shape gets a row at the end of the table with a `{TODO: ...}` description.
3. For each `{TODO: ...}` row, run `python3 helpers/form-types.py --report` and read that shape's block — its target class, its `sh:message`, and its properties marked `REQ`/`opt`. Write the description from those facts, matching the existing rows' style: what the form records, required fields first, then the optional ones, no trailing period. Give the row a real display name too — the generated one is a naive de-camel-casing of the shape's local name (`PetsCareAndFeedingShape` → "Pets Care And Feeding"), so fix it to the label a user would see. Then move the row from the end of the table into the group it belongs with; the ordering is editorial (person-subject forms, then documents, then accounts, then possessions and places, then records), and the script preserves whatever order it finds.
4. Re-read the two paragraphs *below* the generated block — the ones about category extensions and about `cell:Calendar`/`cell:Canvas`/`cell:Map`. They name specific facts (`bhsshapes:MemberShape` as the one member-shape-only shape; `bhscat:BostonHubSociety` declaring a core shape; the three tool kinds having no content model). `--check`'s match line prints the current member-shape-only set, and `cell.ttl` settles the tool kinds. Update the prose if either has changed.
5. Re-run `python3 helpers/form-types.py --check` — it must exit 0.

## Scope

- Only `app-behavior.md`'s Form Types table and the two paragraphs immediately below it. Nothing between the `<!-- BEGIN GENERATED: form-types -->` fences is ever hand-edited — change the ontology or the registry instead, then regenerate.
- Does **not** add, remove or rename a shape, a category, or a template's `cell:formShape`. Those are modeling changes and separate, explicit requests; this command only makes the documentation catch up with them.
- Does **not** touch `README.md`. Per CLAUDE.md's README Coverage rule, README documents what a term *is*; which form types the Add Tool dialog offers is app behavior and lives here. A genuinely new class or property still needs its own README mention — flag that, don't write it here.

## After editing

- Report a concise summary: rows added, removed or re-pointed, and which descriptions you wrote. Don't reprint unchanged rows.
- No `.ttl` file changed, so no version bump — unless step 1 sent you to `helpers/validate.py`, which carries no version either. If the sync revealed a missing SHACL shape or template, say so rather than inventing one.
