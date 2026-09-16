---
id: http://www.example.org/v4/cells/cell-45
title: "Travel"
type: cell-databook
version: 1.0.0
created: 2026-08-30
description: >
  Cell DataBook for folder "Travel" (cell:category: cat:Travel). It is a one-member cell with one
  member entry about :Self — a minimal stub, since "Travel" is a purely organizational category
  node with no content or relationship of its own beyond Alice's required membership. Nested inside
  it is the "Kyoto Trip 2027" cell for a specific trip.
v4:
  category: "cat:Travel"
  creator: ":Self"
  owner: ":Self"
  member:
    id: "http://www.example.org/v4/graphs/graph-64"
    claimant: ":Self"
    subject: ":Self"
    shape: "pshapes:ContactInfoShape"
---

## Graphs

<a id="graph-64"></a>
### Graph 64

#### Overview

This graph is the cell's one required `member` entry — a cell with a single `member` entry in the user's own category-cell tree always has `:Self` as that member (see YAML-6), regardless of what the cell's `subject` is. The "Travel" cell is a purely organizational category node (`cell:category: cat:Travel`) with no relationship or subject of its own beyond Alice's required membership, so this stub carries no further claims. Alice is both the claimant and the subject. It carries her given name, satisfying the `ContactInfoShape` `ctpl:TravelTemplateCell` sets as `cell:memberShape` — no longer deliberately empty.

#### Graph

```turtle
<!-- databook:id: alice-travel-member-graph -->
<!-- databook:graph: http://www.example.org/v4/graphs/graph-64#graph -->
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
