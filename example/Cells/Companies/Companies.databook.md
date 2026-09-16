---
id: http://www.example.org/v4/cells/cell-22
title: "Companies"
type: cell-databook
version: 1.2.0
created: 2026-07-10
description: >
  Cell DataBook for folder "Companies" (cell:category: cat:Companies). It is a
  one-member cell with one member entry about :Self — a minimal stub,
  since "Companies" is a purely organizational category node with no
  content or relationship of its own beyond Alice's required membership.
  Also carries an empty tool graph, since cat:Companies's own TemplateCell
  declares a form tool — the real content
  lives in this category's own leaf cells (Google, ATT) instead.
v4:
  category: "cat:Companies"
  creator: ":Self"
  owner: ":Self"
  member:
    id: "http://www.example.org/v4/graphs/graph-40"
    claimant: ":Self"
    subject: ":Self"
    shape: "pshapes:ContactInfoShape"
  tool:
    - type: "form"
      formTopic: ":Self"
      graph:
        - id: "http://www.example.org/v4/graphs/graph-85"
          claimant: ":Self"
---

## Graphs

<a id="graph-40"></a>
### Graph 40

#### Overview

This graph is the cell's one required `member` entry — a cell with a single `member` entry in the user's own category-cell tree always has `:Self` as that member (see YAML-6), regardless of what the cell's `subject` is — here, Alice herself. The "Companies" cell is a purely organizational category node (`cell:category: cat:Companies`) with no relationship or subject of its own beyond Alice's required membership. Alice is both the claimant and the subject. It carries her given name, satisfying the `ContactInfoShape` `ctpl:CompaniesTemplateCell` sets as `cell:memberShape` — no longer deliberately empty.

#### Graph

```turtle
<!-- databook:id: alice-companies-member-graph -->
<!-- databook:graph: http://www.example.org/v4/graphs/graph-40#graph -->
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

<a id="graph-85"></a>
### Graph 85

#### Overview

This graph is the cell's required tool graph — required since `cat:Companies`'s own `TemplateCell` declares a form tool, even though "Companies" is a purely organizational scaffold cell with no tool content of its own (the real content lives in this category's own leaf cells, Google and ATT, instead). Deliberately empty — no triples at all. Alice is both the claimant and the subject.

#### Graph

```turtle
<!-- databook:id: alice-companies-tool-graph -->
<!-- databook:graph: http://www.example.org/v4/graphs/graph-85#graph -->
```
