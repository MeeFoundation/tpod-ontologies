---
id: http://www.example.org/v4/pods/pod-19
title: "Paula Walker"
type: pod-databook
version: 1.3.0
created: 2026-07-10
description: >
  Pod DataBook for folder "Paula Walker" (pod:category: cat:Employees, reusing its parent "Employees" pod's own origin, mirroring how e.g. "Ginger" reuses its parent "Pets" folder's own category rather than a separately-minted narrower one). It is a two-member pod with member entries about :Self and :Paula_Walker.
v4:
  category: "cat:Employees"
  creator: ":Self"
  owner: ":Self"
  member:
    - id: "http://www.example.org/v4/graphs/graph-20"
      claimant: ":Self"
      subject: ":Self"
      shape: "pshapes:ContactInfoShape"
    - id: "http://www.example.org/v4/graphs/graph-06"
      claimant: ":Self"
      subject: ":Paula_Walker"
      shape: "pshapes:ContactInfoShape"
---

## Graphs

<a id="graph-06"></a>
### Graph 06

#### Overview

This graph captures Alice's record of her colleague Paula Walker in their shared Acme employment graph — one of the pod's two required `member` entries, satisfying `ContactInfoShape`'s required GivenName alongside her existing `rdfs:label` (this pod's category declares no tool, so its content belongs in the member graph; `cat:Employee` has since been deleted entirely, and this pod now reuses `cat:Employees` directly). Alice is the claimant.

#### Graph

```turtle
<!-- databook:id: paula-acme-graph -->
<!-- databook:graph: http://www.example.org/v4/graphs/graph-06#graph -->
@prefix : <http://www.example.org/v4#> .
@prefix persona: <http://mee.foundation/ontologies/persona#> .
@prefix cco: <https://w3id.org/cco-domains/cco/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

:Paula_Walker rdf:type owl:NamedIndividual ,
               persona:Person ;
    rdfs:label "Paula Walker (Acme)"@en ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → GivenName (ContactInfoShape)
        rdf:type cco:ent00000002 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "Paula"
    ] .
```

<a id="graph-20"></a>
### Graph 20

#### Overview

This graph captures Alice Walker's employee identity at Acme. It records her work email address (alice@acme.com) and her Acme social network, which includes colleague Paula Walker. Alice is the claimant.

#### Graph

```turtle
<!-- databook:id: alice-acme-graph -->
<!-- databook:graph: http://www.example.org/v4/graphs/graph-20#graph -->
@prefix : <http://www.example.org/v4#> .
@prefix persona: <http://mee.foundation/ontologies/persona#> .
@prefix cco: <https://w3id.org/cco-domains/cco/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

:Self rdf:type owl:NamedIndividual ,
               persona:Person .

:Paula_Walker rdf:type owl:NamedIndividual ,
               persona:Person .

:Self rdfs:comment "Alice Walker's persona for her employment at Acme."@en ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → GivenName (ContactInfoShape)
        rdf:type cco:ent00000002 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "Alice"
    ] ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → AlternateName
        rdf:type cco:ent00000006 ;  # AlternateName
        <https://w3id.org/cco-domains/cco/ont00001765> "Alice Walker"
    ] ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → Email
        rdf:type cco:ent00000024 ;  # Email
        <https://w3id.org/cco-domains/cco/ont00001765> "alice@acme.com"  # has text value
    ] ;

    persona:hasSocialNetwork :Alice_Acme_Network .


:Alice_Acme_Network rdf:type owl:NamedIndividual ,
                             cco:ont00001183 ;  # Social Network
    rdfs:label "Alice Walker's Acme connections"@en ;
    <http://purl.obolibrary.org/obo/BFO_0000115> :Paula_Walker .  # has member part
```
