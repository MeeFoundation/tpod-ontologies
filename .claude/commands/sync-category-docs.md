---
description: Reconcile category.ttl leaf-category rdfs:comment text against README.md's Personal/Organizational Categories descriptions (README is authoritative)
---

Reconcile `category.ttl`'s `rdfs:comment` text for every leaf category under `cat:Person` and `cat:Organization` against the corresponding bullet description in `README.md`'s **Personal Categories** and **Organizational Categories** sections (under the "Pod Categories" heading).

**README.md is authoritative.** Where the two differ in substance, rewrite the `category.ttl` comment to match the README's wording — not the other way around. This is a one-directional sync: README → category.ttl.

## Scope

- Covers every `cat:X` concept reachable from `cat:Person` by following `skos:broader` (asserted child → parent) one or more steps, and likewise for `cat:Organization` — i.e. every concept listed as a bullet/sub-bullet in the two README sections. `category.ttl` has no `cat:Category` class to check against — every concept is a plain `skos:Concept` individual, scoped to `cat:CategoryScheme` via `skos:inScheme`.
- Does **not** touch `cat:Person` or `cat:Organization` themselves (the two top concepts, `skos:hasTopConcept` of `cat:CategoryScheme`) — only the narrower concepts reachable from them.
- Does **not** add or remove categories, or rename anything — this command only reconciles description *text*. Renames and additions/removals are separate, explicit requests.

## Method

1. Read `category.ttl` and extract every `cat:X rdfs:comment "..."@en` under the Personal and Organizational subclass sections.
2. Read `README.md`'s Personal Categories and Organizational Categories bullet lists and extract each category's description text.
3. For each class, compare the two ignoring pure formatting differences (README wraps class names in backticks with `cat:`/`pod:` prefixes, uses bold for labels, and starts each description lowercase since it follows an em dash — none of that is a substantive difference). Flag as a real mismatch: added/removed clauses, different examples, different cross-references, different scope statements.
4. Where a mismatch is real, replace the `category.ttl` comment with text matching the README's content — reformatted as a standalone sentence (capitalized first letter, trailing period), in the same person/voice the surrounding `category.ttl` comments already use.
5. If a category is missing from README entirely, or a `category.ttl` class has no bullet in either README section at all, don't guess a fix — report it instead (that's a coverage gap, not a wording sync, and is handled by the existing "README Coverage" rule in CLAUDE.md).

## After editing

- Bump `category.ttl`'s minor version per CLAUDE.md's versioning rule (`owl:versionIRI`, `dc:date`, `owl:versionInfo`) and list which classes' comments were changed in the changelog entry.
- Validate the file parses: `riot --validate category.ttl` (fall back to `python3 -c "import rdflib; rdflib.Graph().parse('category.ttl', format='turtle')"` if `riot` isn't available).
- Report a concise summary: which classes were changed and a one-line description of each change. Don't dump full before/after text for unchanged classes.
