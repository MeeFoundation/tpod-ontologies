---
id: http://www.example.org/v4/cells/cell-06
title: "SSN"
type: cell-databook
version: 2.0.0
created: 2026-07-10
description: >
  Cell DataBook for folder "SSN" (cell:category: cat:SSN). It is a one-member cell with one
  member entry about :Self and one topic graph about :Self (the cell's subject), carrying
  Alice's Social Security number.
v4:
  category: "cat:SSN"
  creator: ":Self"
  owner: ":Self"
  member:
    id: "http://www.example.org/v4/graphs/graph-23"
    claimant: ":Self"
    subject: ":Self"
    shape: "pshapes:ContactInfoShape"
  tool:
    - type: "form"
      formTopic: ":Self"
      graph:
        - id: "http://www.example.org/v4/graphs/graph-80"
          claimant: ":Self"
          shape: "pshapes:SSNShape"
---

## Graphs

<a id="graph-23"></a>
### Graph 23

#### Overview

This graph is the cell's one required `member` entry — a cell with a single `member` entry in the user's own category-cell tree always has `:Self` as that member (see YAML-6). Alice is both the claimant and the subject. It carries her given name, satisfying the `ContactInfoShape` every templated cell's `member` content is now expected to conform to (`cell:memberShape`) — no longer the SSN itself, which now lives in this cell's tool graph instead (graph 80).

#### Graph

```turtle
<!-- databook:id: alice-ssn-member-graph -->
<!-- databook:graph: http://www.example.org/v4/graphs/graph-23#graph -->
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

<a id="graph-80"></a>
### Graph 80

#### Overview

This graph captures Alice Walker's Social Security Administration record — moved here, as this cell's tool content, from the cell's former `member` graph-23. Alice self-enters her SSN (123-45-6788) from her physical Social Security card. The SSA is not a PDN node, so this data is self-claimed rather than received from the SSA directly. Validated by `shacl/persona-shacl.ttl`'s `:SSNShape` (reused directly as this cell's declared tool's `cell:formShape`, since the SSN designator has no separate document class of its own). Alice is the claimant.

#### Graph

```turtle
<!-- databook:id: alice-ssa-graph -->
<!-- databook:graph: http://www.example.org/v4/graphs/graph-80#graph -->
@prefix : <http://www.example.org/v4#> .
@prefix persona: <http://mee.foundation/ontologies/persona#> .
@prefix cco: <https://w3id.org/cco-domains/cco/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

:Self rdf:type owl:NamedIndividual ,
               persona:Person .

:Self rdfs:comment "Alice Walker's persona for her Social Security Administration record."@en ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → SSN
        rdf:type cco:ent00000008 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "123-45-6788"
    ] .
```
