---
id: http://www.example.org/v4/pods/pod-16
title: "Bob Johnson"
type: pod-databook
version: 1.3.0
created: 2026-07-10
description: >
  Pod DataBook for folder "Bob Johnson" (pod:category: podcat:Others). It is a two-member pod with four members (two about :Bob_Johnson and two about :Self).
v4:
  category: "podcat:Others"
  creator: ":Self"
  owner: ":Self"
  serviceTag:
    - namespace: "foundation.mee.applecontacts"
      key: "group"
      value: "Christmas List"
  member:
    - id: "http://www.example.org/v4/graphs/graph-02"
      claimant: ":Bob_Johnson"
      subject: ":Bob_Johnson"
      shape: "pshapes:ContactInfoShape"
    - id: "http://www.example.org/v4/graphs/graph-12"
      claimant: ":Self"
      subject: ":Self"
      shape: "pshapes:ContactInfoShape"
    - id: "http://www.example.org/v4/graphs/graph-04"
      claimant: ":Self"
      subject: ":Bob_Johnson"
      shape: "pshapes:ContactInfoShape"
    - id: "http://www.example.org/v4/graphs/graph-08"
      claimant: ":Bob_Johnson"
      subject: ":Self"
      shape: "pshapes:ContactInfoShape"
---

## Graphs

<a id="graph-02"></a>
### Graph 02

#### Overview

This graph captures Bob Johnson's self-claimed Bob-graph persona, transmitted from Bob's own instance of the app to Alice's over the PDN. It records Bob's name and his social network link to Alice. Bob is the claimant.

#### Graph

```turtle
<!-- databook:id: bob-bob-bob-graph -->
<!-- databook:graph: http://www.example.org/v4/graphs/graph-02#graph -->
@prefix : <http://www.example.org/v4#> .
@prefix persona: <http://mee.foundation/ontologies/persona#> .
@prefix cco: <https://w3id.org/cco-domains/cco/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

:Bob_Johnson rdf:type owl:NamedIndividual ,
              persona:Person ;
    rdfs:label "Bob Johnson (Bob)"@en ;
    rdfs:comment "Bob Johnson's self-claimed persona in the 1:1 Bob graph."@en ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → GivenName
        rdf:type cco:ent00000002 ;  # GivenName
        <https://w3id.org/cco-domains/cco/ont00001765> "Bob"  # has text value
    ] ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → FamilyName
        rdf:type cco:ent00000004 ;  # FamilyName
        <https://w3id.org/cco-domains/cco/ont00001765> "Johnson"  # has text value
    ] ;

    persona:hasSocialNetwork :Bob_Bob_Network .


:Bob_Bob_Network rdf:type owl:NamedIndividual ,
                          cco:ont00001183 ;  # Social Network
    rdfs:label "Bob Johnson's Bob connection"@en ;
    <http://purl.obolibrary.org/obo/BFO_0000115> :Self .  # has member part → Alice
```

<a id="graph-04"></a>
### Graph 04

#### Overview

This graph captures Alice's record of Bob Johnson in their 1:1 relationship graph. Alice notes Bob's favorite drink and given name, the latter required by the `ContactInfoShape` every templated pod's `member` content is now expected to conform to (`pod:memberShape`). Alice is the claimant.

#### Graph

```turtle
<!-- databook:id: bob-bob-alice-graph -->
<!-- databook:graph: http://www.example.org/v4/graphs/graph-04#graph -->
@prefix : <http://www.example.org/v4#> .
@prefix persona: <http://mee.foundation/ontologies/persona#> .
@prefix cco: <https://w3id.org/cco-domains/cco/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

:Bob_Johnson rdf:type owl:NamedIndividual ,
              persona:Person ;
    rdfs:label "Bob Johnson (Bob-colleague-of-alice)"@en ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → GivenName (ContactInfoShape)
        rdf:type cco:ent00000002 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "Bob"
    ] ;

    <https://w3id.org/cco-domains/cco/ont00001917> [  # described by → Person Note
        rdf:type cco:ent00000048 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "Fav drink: oat milk cappuccino"
    ] .
```

<a id="graph-08"></a>
### Graph 08

#### Overview

This graph captures Bob's record of Alice in their 1:1 relationship graph, transmitted from Bob's own instance of the app to Alice's over the PDN. Bob notes Alice's favorite drink and given name, the latter required by the `ContactInfoShape` every templated pod's `member` content is now expected to conform to (`pod:memberShape`). Bob is the claimant.

#### Graph

```turtle
<!-- databook:id: alice-bob-bob-graph -->
<!-- databook:graph: http://www.example.org/v4/graphs/graph-08#graph -->
@prefix : <http://www.example.org/v4#> .
@prefix persona: <http://mee.foundation/ontologies/persona#> .
@prefix cco: <https://w3id.org/cco-domains/cco/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

:Self rdf:type owl:NamedIndividual ,
               persona:Person .

:Self <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → GivenName (ContactInfoShape)
        rdf:type cco:ent00000002 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "Alice"
    ] ;

    <https://w3id.org/cco-domains/cco/ont00001917> [  # described by → Person Note
        rdf:type cco:ent00000048 ;
        <https://w3id.org/cco-domains/cco/ont00001765> "Favorite drink: pepsi"
    ] .
```

<a id="graph-12"></a>
### Graph 12

#### Overview

This graph captures Alice Walker's self-claimed persona in her 1:1 relationship with Bob Johnson. It records the name Alice presents to Bob and her social network link to him. Alice is the claimant.

#### Graph

```turtle
<!-- databook:id: alice-bob-alice-graph -->
<!-- databook:graph: http://www.example.org/v4/graphs/graph-12#graph -->
@prefix : <http://www.example.org/v4#> .
@prefix persona: <http://mee.foundation/ontologies/persona#> .
@prefix cco: <https://w3id.org/cco-domains/cco/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

:Self rdf:type owl:NamedIndividual ,
               persona:Person .

:Self rdfs:comment "Alice Walker's persona for her 1:1 relationship with Bob."@en ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → AlternateName
        rdf:type cco:ent00000006 ;  # AlternateName
        <https://w3id.org/cco-domains/cco/ont00001765> "Alice Walker"
    ] ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → GivenName
        rdf:type cco:ent00000002 ;  # GivenName
        <https://w3id.org/cco-domains/cco/ont00001765> "Alice"  # has text value
    ] ;

    <https://w3id.org/cco-domains/cco/ont00001879> [  # designated by → FamilyName
        rdf:type cco:ent00000004 ;  # FamilyName
        <https://w3id.org/cco-domains/cco/ont00001765> "Walker"  # has text value
    ] ;

    persona:hasSocialNetwork :Alice_Bob_Network .


:Alice_Bob_Network rdf:type owl:NamedIndividual ,
                             cco:ont00001183 ;  # Social Network
    rdfs:label "Alice Walker's Bob connection"@en ;
    <http://purl.obolibrary.org/obo/BFO_0000115> :Bob_Johnson .  # has member part
```
