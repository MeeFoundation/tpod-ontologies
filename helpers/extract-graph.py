#!/usr/bin/env python3
"""
extract-graph.py — print one graph's fenced turtle block from a
pod-databook file that may contain several (one per embedded graph),
matched by its known `<!-- databook:graph: {graph_id}#graph -->` marker.

Why this exists: a pod with more than one embedded graph (e.g. the Medical
Appointment pod, which has three) would have its sibling graphs' triples
wrongly pulled in by a whole-file extraction — but validation's template pass
checks one graph's data in isolation against a per-template SHACL shape. This
is the single-graph counterpart to extract-all.py's whole-tree extraction;
both share the same fence parser, databook_graphs.iter_graph_blocks().

Usage: python3 helpers/extract-graph.py <pod_file.databook.md> <graph-id-or-local-name>
Output: the matched graph's raw Turtle content on stdout.
"""
import sys

import yaml

from databook_graphs import extract_graph_block, find_graph_entry, graph_entries, split_frontmatter


def main():
    if len(sys.argv) != 3:
        sys.exit("Usage: helpers/extract-graph.py <pod_file.databook.md> <graph-id-or-local-name>")
    path, graph_arg = sys.argv[1], sys.argv[2]
    text = open(path, encoding="utf-8").read()
    fm_text, _, body = split_frontmatter(text)
    fm = yaml.safe_load(fm_text)
    v4 = fm.get("v4") or {}
    entries = graph_entries(v4)
    match = find_graph_entry(entries, graph_arg)
    if not match:
        sys.exit(f"No v4.member or v4.tool[].graph entry with id/local-name {graph_arg!r} in {path}")
    lines = extract_graph_block(body, f"{match['id']}#graph")
    if lines is None:
        sys.exit(f"No turtle block found for {match['id']!r} in {path}")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
