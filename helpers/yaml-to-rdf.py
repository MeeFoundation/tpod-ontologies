#!/usr/bin/env python3
"""
yaml-to-rdf.py  —  Synthesize cell: triples from the `v4.` YAML
frontmatter of cell-databooks.

Why this exists: Turtle-block extraction only pulls fenced Turtle out of a
DataBook — but cell-databook files carry most of their content as `v4.`
YAML frontmatter, not Turtle. Without this script, cell:Cell individuals
(and cell:MemberGraph's subject/claimant) never appear in the graph SHACL
validates, so shacl/cell-shacl.ttl's :MemberGraphShape never fires against real
instance data. This script closes that gap by mapping each `v4.` field to
its corresponding ontology property, matching the mapping tables
documented in cell-databook.md's "The `v4` Block" section.

There is no category-side synthesis here at all — category.ttl 1.31.0
deleted cat:Folder and its subclasses cat:CategoryDefined/cat:UserDefined
outright, along with cat:child/cat:cell/cat:category/cat:catType/cat:label.
A cell's tree position is not modelled at all: at runtime it is per-member
state in that member's own store, and in this repo's scaffolding it is simply
which folder the cell-databook physically lives in, with no RDF individual
representing either. The only remaining RDF-level record of a cell's
classification is
cell:category (cell.ttl 3.20.0), read directly from the explicit `v4.category`
YAML field below — never derived from filename-parsing.

Since graph-databooks were merged into their owning cell-databooks (each
graph's Turtle content and Overview now live in that cell file's body; its
`id`/`claimant`/`shape`, plus the `subject` a member entry carries
list calls for, now live directly on that same graph's own
`v4.member`/`v4.tool[].graph` entry — see cell-databook.md's "Graph Ids
and Named Graphs" section), there is no separate `example/graphs/*.databook.md`
glob any more: `process_cell_databook` below also emits the same triples per
`member`/`tool[].graph` entry that a standalone graph-databook file's frontmatter
used to supply.

A graph's `claimant` and its about-ness value are typed on its plain
`v4.member[]`/`v4.tool[].graph[].id`, not that id + "#graph" — matching cell.ttl's
cell:claimant/cell:subject doc comments, and the IRI
cell:member/cell:formGraph actually reference.

Usage:   python3 helpers/yaml-to-rdf.py [repo-root] > yaml-data.ttl
Output:  Turtle triples on stdout — merge with `riot` alongside data extracted
         via `helpers/extract-all.py` (see example.md's Validation section).

Requires: pip install pyyaml
"""

import os, re, sys, yaml, glob

from databook_graphs import process_cell_databook

def frontmatter(path):
    text = open(path, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    return yaml.safe_load(m.group(1)) if m else None


def main(root):
    triples = []

    for path in sorted(
        glob.glob(os.path.join(root, "example", "Cells", "**", "*.databook.md"), recursive=True)
    ):
        if "under-development" in path.split(os.sep):
            continue
        fm = frontmatter(path)
        if not fm or fm.get("type") != "cell-databook":
            continue
        process_cell_databook(fm, triples)

    print("\n".join(triples))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
