---
id: http://www.example.org/tpod/pods/pod-29
title: "People"
type: pod-databook
version: 1.1.0
created: 2026-07-10
description: >
  Pod DataBook for folder "People" (pod:category: podcat:People). It is a
  one-member pod with one member entry about :Self — a purely
  organizational category node with no relationship of its own beyond
  Alice's required membership, though that member entry now carries a
  minimal ContactInfo-style claim (organization name,
  email), per podcat:People's own pod:TemplatePod.
tpod:
  category: "podcat:People"
  creator: ":Self"
  owner: ":Self"
  member:
    id: "http://www.example.org/tpod/graphs/graph-47"
    claimant: ":Self"
    subject: ":Self"
    shape: "pshapes:ContactInfoShape"
---

## Graphs

<a id="graph-47"></a>
### Graph 47

#### Overview

This graph is the pod's one required `member` entry — a pod with a single `member` entry in the user's own category-pod tree always has `:Self` as that member (see YAML-6), regardless of what the pod's `subject` is — here, Alice herself. The "People" pod is a purely organizational category node (`pod:category: podcat:People`) with no relationship or subject of its own beyond Alice's required membership. Alice is both the claimant and the subject. It carries her given name, plus a minimal organization name and email, so `:Self` satisfies the `ContactInfoShape` `podcat:People`'s own `pod:TemplatePod` expects of its member content (`pod:memberShape`) — no longer deliberately empty now that this requirement applies.

#### Graph

```turtle
<!-- databook:id: alice-people-member-graph -->
<!-- databook:graph: http://www.example.org/tpod/graphs/graph-47#graph -->
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
