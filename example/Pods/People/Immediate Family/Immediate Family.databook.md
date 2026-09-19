---
id: http://www.example.org/v4/pods/pod-30
title: "Immediate Family"
type: pod-databook
version: 1.1.0
created: 2026-07-10
description: >
  Pod DataBook for folder "Immediate Family" (pod:category: podcat:ImmediateFamily). It is a
  one-member pod with one member entry about :Self — a purely
  organizational category node with no relationship of its own beyond
  Alice's required membership, though that member entry now carries a
  minimal ContactInfo-style claim (given name,
  organization name, email), per podcat:ImmediateFamily's own pod:TemplatePod.
v4:
  category: "podcat:ImmediateFamily"
  creator: ":Self"
  owner: ":Self"
  member:
    id: "http://www.example.org/v4/graphs/graph-48"
    claimant: ":Self"
    subject: ":Self"
    shape: "pshapes:ContactInfoShape"
---

## Graphs

<a id="graph-48"></a>
### Graph 48

#### Overview

This graph is the pod's one required `member` entry — a pod with a single `member` entry in the user's own category-pod tree always has `:Self` as that member (see YAML-6), regardless of what the pod's `subject` is — here, Alice herself. The "Immediate Family" pod is a purely organizational category node (`pod:category: podcat:ImmediateFamily`) with no relationship or subject of its own beyond Alice's required membership. Alice is both the claimant and the subject. It carries her given name (required by `ContactInfoShape`, `pod:memberShape`), plus an optional organization name and email — no longer deliberately empty now that this requirement applies.

#### Graph

```turtle
<!-- databook:id: alice-immediate-family-member-graph -->
<!-- databook:graph: http://www.example.org/v4/graphs/graph-48#graph -->
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
    ] ,
    [  # designated by → OrganizationName (ContactInfoShape)
        rdf:type cco:ent00000047 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "Acme"
    ] ,
    [  # designated by → EmailAddress (ContactInfoShape)
        rdf:type cco:ent00000024 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "alice@acme.com"
    ] .
```
