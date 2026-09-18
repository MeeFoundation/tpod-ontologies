# PR Notes — Two-Relation Identifier Pattern (Government-ID Numbers)

**What this PR does:** implements the two-relation form for the driver's-license and passport numbers, the pattern we agreed on in Discord (2026-07-23). It touches three files: the two gov-ID databooks and their SHACL shapes. **Please read §1 before merging** — it's one genuine modeling change (everything else is mechanical), and it sets a pattern we'll both reuse.

---

## 1. The one conceptual change (please read this)

**Before:** the ID number hung off the *document* as an anonymous node — the document was `designated by` the number.

**After:** the ID number is a single *named* node with **two relations** pointing at it:
- **the Person is `designated by` it** (`ont00001879`) — because the number's uniqueness runs to the person (one license number, one bearer). This is the path person-matching traverses.
- **the document `is carrier of` it** (`BFO_0000101`) — because the physical card/booklet carries the number. This is the physical-carriage fact.

One node, two relations — nothing is lost, and cross-source person-matching gets one reliable path to the identifier.

**Before / after (passport number):**
```turtle
# BEFORE — number is an anonymous node the document designates
:Alice_US_Passport
    ont00001879 [ rdf:type cco:ent00000066 ; ont00001765 "123456789" ] .

# AFTER — number is a named node; Person designates it, document carries it
:Self
    ont00001879 :Alice_Passport_Number .                    # Person designated by
:Alice_US_Passport
    obo:BFO_0000101 :Alice_Passport_Number .                # document is carrier of
:Alice_Passport_Number rdf:type cco:ent00000066 ;
    ont00001765 "123456789" .
```

Why it matters: it aligns with the CCO term definitions ("a Person Identifier issued to a **person**") and makes the person the anchor for identity resolution, while still recording that the document is what physically bears the number.

## 2. Scope — deliberately narrow

Applied **only** to the two Person-designating ID numbers: Drivers License Number (`cco:ent00000065`) and Passport Number (`cco:ent00000066`). **Not** applied to Place of Birth (067), Issuing Jurisdiction (068), or the issue/expiration dates (069/070) — those describe the document or the event, not the person, so person-designation would be semantically wrong. They stay exactly as they are.

## 3. Files changed

- `example/contexts/self.self(passport)(federal)(19).databook.md` — passport number → two-relation form (`:Alice_Passport_Number`).
- `example/contexts/self.self(california-dmv)(state)(15).databook.md` — DL number → two-relation form (`:Alice_DL_Number`).
- `pod-templates-shacl.ttl` — the `DriversLicenseDocumentShape` and `PassportDocumentShape` number constraints: the `sh:path` for the number changed from `ont00001879` (designated by) to `BFO_0000101` (is carrier of), since the document now *carries* the number rather than *designating* it. Cardinality (exactly 1) unchanged.

All three files parse clean (rdflib 7.x).

## 4. Heads-up: the SHACL is strict (a deliberate choice)

The updated shapes **require** the new two-relation form — the number must be reached via `is carrier of` on the document. Both databooks in this PR are already converted, so they validate cleanly. But note the consequence: **any other context file still using the old single-relation form (number designated-by the document) would now fail validation** against these shapes.

I chose strict rather than backward-compatible on purpose: these are the only two government-ID databooks, both are converted in this PR, and enforcing one form keeps the shapes simple and the pattern unambiguous going forward. This is slightly stricter than my earlier Discord note ("your current pattern keeps working") — that reassurance was about the *conformance profile* treating document-attached identifiers as a recognized source pattern, which still holds at the profile level; it's only these two per-template document shapes that now require the new form.

If you'd rather the shapes accept **either** form (a one-line `sh:or` change so old-style data still validates), just say so and I'll send a follow-up. Otherwise, strict stands.

## 5. Verification (run to confirm)

```bash
# both databooks + shapes parse
python3 -c "from rdflib import Graph; [Graph().parse(f, format='turtle') for f in ['pod-templates-shacl.ttl']]; print('shapes OK')"

# confirm the two relations are present on each number node
grep -n "BFO_0000101\|:Alice_Passport_Number\|:Alice_DL_Number" example/contexts/self.self*.databook.md
```
(The databooks embed Turtle in Markdown fences; extract the fenced block before parsing, or validate via your existing databook tooling.)

## 6. Not in this PR

- Term migrations (065–073, date property patterns) — you already did these; nothing to do.
- `cco:ent00000054` (expiration date) still on the old form in `persona.ttl` and `draw.py` — a small independent sweep to the `ent00000070` predicate pattern (which you've already applied in the databooks). Happy to fold into a follow-up if useful, or it's a quick one for you.
