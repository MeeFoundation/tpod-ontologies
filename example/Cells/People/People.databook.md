---
id: http://www.example.org/v4/cells/cell-29
title: "People"
type: cell-databook
version: 1.1.0
created: 2026-07-10
description: >
  Cell DataBook for folder "People" (cell:category: cat:People). It is a
  one-member cell with one member entry about :Self — a purely
  organizational category node with no relationship of its own beyond
  Alice's required membership, though that member entry now carries a
  minimal ContactInfo-style claim (organization name,
  email), per cat:People's own cell:TemplateCell.
v4:
  category: "cat:People"
  creator: ":Self"
  owner: ":Self"
  member:
    id: "http://www.example.org/v4/graphs/graph-47"
    claimant: ":Self"
    subject: ":Self"
    shape: "pshapes:ContactInfoShape"
---

## Graphs

<a id="graph-47"></a>
### Graph 47

#### Overview

This graph is the cell's one required `member` entry — a cell with a single `member` entry in the user's own category-cell tree always has `:Self` as that member (see YAML-6), regardless of what the cell's `subject` is — here, Alice herself. The "People" cell is a purely organizational category node (`cell:category: cat:People`) with no relationship or subject of its own beyond Alice's required membership. Alice is both the claimant and the subject. It carries her given name, plus a minimal organization name and email, so `:Self` satisfies the `ContactInfoShape` `cat:People`'s own `cell:TemplateCell` expects of its member content (`cell:memberShape`) — no longer deliberately empty now that this requirement applies.

#### Graph

```turtle
<!-- databook:id: alice-people-member-graph -->
<!-- databook:graph: http://www.example.org/v4/graphs/graph-47#graph -->
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
