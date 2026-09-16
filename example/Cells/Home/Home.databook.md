---
id: http://www.example.org/v4/cells/cell-48
title: "Home"
type: cell-databook
version: 1.1.0
created: 2026-09-03
description: >
  Cell DataBook for folder "Home" (cell:category: cat:Home). It is a
  one-member cell with one member entry about :Self — a minimal stub,
  since "Home" is a purely organizational category node with no
  content or relationship of its own beyond Alice's required membership.
  also carries an empty tool graph, since cat:Home's own
  TemplateCell declares a form tool — the real content
  lives in this category's own leaf cells (Paradise, Boston) instead.
v4:
  category: "cat:Home"
  creator: ":Self"
  owner: ":Self"
  member:
    id: "http://www.example.org/v4/graphs/graph-71"
    claimant: ":Self"
    subject: ":Self"
    shape: "pshapes:ContactInfoShape"
  tool:
    - type: "form"
      formTopic: ":Self"
      graph:
        - id: "http://www.example.org/v4/graphs/graph-87"
          claimant: ":Self"
---

## Graphs

<a id="graph-71"></a>
### Graph 71

#### Overview

This graph is the cell's one required `member` entry — a cell with a single `member` entry in the user's own category-cell tree always has `:Self` as that member (see YAML-6), regardless of what the cell's `subject` is — here, Alice herself. The "Home" cell is a purely organizational category node (`cell:category: cat:Home`) with no relationship or subject of its own beyond Alice's required membership. Alice is both the claimant and the subject. It carries her given name, satisfying the `ContactInfoShape` now that `ctpl:HomeTemplateCell` sets `cell:memberShape` to it — no longer deliberately empty.

#### Graph

```turtle
<!-- databook:id: alice-home-member-graph -->
<!-- databook:graph: http://www.example.org/v4/graphs/graph-71#graph -->
@prefix : <http://www.example.org/v4#> .
@prefix cco: <https://w3id.org/cco-domains/cco/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix persona: <http://mee.foundation/ontologies/persona#> .

:Self rdf:type owl:NamedIndividual ,
               persona:Person .

:Self <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → GivenName (ContactInfoShape)
        rdf:type cco:ent00000002 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "Alice"
    ] .
```

<a id="graph-87"></a>
### Graph 87

#### Overview

This graph is the cell's required tool graph — required since `cat:Home`'s own `TemplateCell` declares a form tool, even though "Home" is a purely organizational scaffold cell with no topic content of its own (the real content lives in this category's own leaf cells, Paradise and Boston, instead). Deliberately empty — no triples at all. Alice is both the claimant and the subject.

#### Graph

```turtle
<!-- databook:id: alice-home-tool-graph -->
<!-- databook:graph: http://www.example.org/v4/graphs/graph-87#graph -->
```
