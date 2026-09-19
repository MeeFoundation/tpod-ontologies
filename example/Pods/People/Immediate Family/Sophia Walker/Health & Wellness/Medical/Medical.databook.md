---
id: http://www.example.org/tpod/pods/pod-31
title: "Medical"
type: pod-databook
version: 1.1.0
created: 2026-07-10
description: >
  Pod DataBook for folder "Medical" (pod:category: podcat:Medical). It is a
  one-member pod with one member entry about :Self — a minimal stub,
  since "Medical" is a purely organizational category node with no
  content or relationship of its own beyond Alice's required membership.
tpod:
  category: "podcat:Medical"
  creator: ":Self"
  owner: ":Self"
  member:
    id: "http://www.example.org/tpod/graphs/graph-49"
    claimant: ":Self"
    subject: ":Self"
    shape: "pshapes:ContactInfoShape"
---

## Graphs

<a id="graph-49"></a>
### Graph 49

#### Overview

This graph is the pod's one required `member` entry — a pod with a single `member` entry in the user's own category-pod tree always has `:Self` as that member (see YAML-6), regardless of what the pod's `subject` is — here, Alice herself. The "Medical" pod is a purely organizational category node (`pod:category: podcat:Medical`) with no relationship or subject of its own beyond Alice's required membership, so this stub carries no further claims. Alice is both the claimant and the subject. It carries her given name, satisfying the `ContactInfoShape` `ctpl:MedicalTemplatePod` sets as `pod:memberShape` — no longer deliberately empty.

#### Graph

```turtle
<!-- databook:id: alice-medical-member-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-49#graph -->
@prefix : <http://www.example.org/tpod#> .
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
