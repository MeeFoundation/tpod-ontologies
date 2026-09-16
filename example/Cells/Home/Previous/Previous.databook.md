---
id: http://www.example.org/v4/cells/cell-49
title: "Previous"
type: cell-databook
version: 1.0.0
created: 2026-09-03
description: >
  Cell DataBook for folder "Previous" (cell:category: cat:Previous). It is a
  one-member cell with one member entry about :Self — a minimal stub,
  since "Previous" is a purely organizational category node with no
  content or relationship of its own beyond Alice's required membership.
v4:
  category: "cat:Previous"
  creator: ":Self"
  owner: ":Self"
  member:
    id: "http://www.example.org/v4/graphs/graph-72"
    claimant: ":Self"
    subject: ":Self"
    shape: "pshapes:ContactInfoShape"
---

## Graphs

<a id="graph-72"></a>
### Graph 72

#### Overview

This graph is the cell's one required `member` entry — a cell with a single `member` entry in the user's own category-cell tree always has `:Self` as that member (see YAML-6), regardless of what the cell's `subject` is — here, Alice herself. The "Previous" cell is a purely organizational category node (`cell:category: cat:Previous`) with no relationship or subject of its own beyond Alice's required membership, so this stub carries no further claims. Alice is both the claimant and the subject. It carries her given name, satisfying the `ContactInfoShape` `ctpl:PreviousTemplateCell` sets as `cell:memberShape` — no longer deliberately empty.

#### Graph

```turtle
<!-- databook:id: alice-previous-member-graph -->
<!-- databook:graph: http://www.example.org/v4/graphs/graph-72#graph -->
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
