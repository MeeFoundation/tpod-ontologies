---
id: http://www.example.org/v4/cells/cell-24
title: "Banking & Payments Firms"
type: cell-databook
version: 1.3.0
created: 2026-07-10
description: >
  Cell DataBook for folder "Banking & Payments Firms" (cell:category: cat:BankingPayments). It is a
  one-member cell with one member entry about :Self — a minimal stub,
  since "Banking & Payments Firms" is a purely organizational category node with no
  content or relationship of its own beyond Alice's required membership.
  Also carries an empty tool graph, since cat:BankingPayments's own TemplateCell
  declares a form tool — the real content
  lives in this category's own leaf cell (Citibank) instead.
v4:
  category: "cat:BankingPayments"
  creator: ":Self"
  owner: ":Self"
  member:
    id: "http://www.example.org/v4/graphs/graph-42"
    claimant: ":Self"
    subject: ":Self"
    shape: "pshapes:ContactInfoShape"
  tool:
    - type: "form"
      formTopic: ":Self"
      graph:
        - id: "http://www.example.org/v4/graphs/graph-86"
          claimant: ":Self"
---

## Graphs

<a id="graph-42"></a>
### Graph 42

#### Overview

This graph is the cell's one required `member` entry — a cell with a single `member` entry in the user's own category-cell tree always has `:Self` as that member (see YAML-6), regardless of what the cell's `subject` is — here, Alice herself. The "Banking & Payments Firms" cell is a purely organizational category node (`cell:category: cat:BankingPayments`) with no relationship or subject of its own beyond Alice's required membership. Alice is both the claimant and the subject. It carries her given name, satisfying the `ContactInfoShape` `ctpl:BankingPaymentsTemplateCell` sets as `cell:memberShape` — no longer deliberately empty.

#### Graph

```turtle
<!-- databook:id: alice-banking-payments-member-graph -->
<!-- databook:graph: http://www.example.org/v4/graphs/graph-42#graph -->
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

<a id="graph-86"></a>
### Graph 86

#### Overview

This graph is the cell's required tool graph — required since `cat:BankingPayments`'s own `TemplateCell` declares a form tool, even though "Banking & Payments Firms" is a purely organizational scaffold cell with no topic content of its own (the real content lives in this category's own leaf cell, Citibank, instead). Deliberately empty — no triples at all. Alice is both the claimant and the subject.

#### Graph

```turtle
<!-- databook:id: alice-banking-payments-tool-graph -->
<!-- databook:graph: http://www.example.org/v4/graphs/graph-86#graph -->
```
