---
id: http://www.example.org/v4/cells/cell-41
title: "Ginger"
type: cell-databook
version: 1.5.0
created: 2026-08-22
description: >
  Cell DataBook for folder "Ginger" (cell:category: cat:Pets). A user-defined instance folder for Alice's specific cat, Ginger, nested under the generic Pets category — mirroring how e.g. "Bob Johnson" reuses its parent "Others" folder's own origin class rather than being Custom. It is a one-member cell with one member entry about :Self and one graph about :Ginger (the cell's subject), typed pets:Pet and carrying her name, species, breed, birth date, current body weight, sex, and spay/neuter status.
v4:
  category: "cat:Pets"
  creator: ":Self"
  owner: ":Self"
  userTag:
    - "Ginger"
  member:
    id: "http://www.example.org/v4/graphs/graph-36"
    claimant: ":Self"
    subject: ":Self"
    shape: "pshapes:ContactInfoShape"
  tool:
    - type: "form"
      formTopic: ":Ginger"
      graph:
        - id: "http://www.example.org/v4/graphs/graph-37"
          claimant: ":Self"
          shape: "petshapes:PetShape"
---

## Graphs

<a id="graph-36"></a>
### Graph 36

#### Overview

This graph is the cell's one required `member` entry — a cell with a single `member` entry in the user's own category-cell tree always has `:Self` as that member (see YAML-6), regardless of what the cell's `subject` is — here, Ginger herself. Alice is both the claimant and the subject. It carries her given name, plus a minimal organization name and email, so `:Self` satisfies the `ContactInfoShape` every templated cell's `member` content is now expected to conform to (`cell:memberShape`) — no longer deliberately empty now that this requirement applies.

#### Graph

```turtle
<!-- databook:id: alice-ginger-member-graph -->
<!-- databook:graph: http://www.example.org/v4/graphs/graph-36#graph -->
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

<a id="graph-37"></a>
### Graph 37

#### Overview

This graph captures Alice's basic claim about Ginger herself — just enough to back the cell's `subject: ":Ginger"` with a real graph (see YAML-4) — and, validated by `pets:Pet`'s SHACL shape (`other/shacl/pets-shacl.ttl`'s `:PetShape`), identifies her name, what kind of pet she is (species — a real NCBITaxon class IRI — and breed — a real VBO class IRI, here VBO's own "Mixed Breed (Cat)" class, since Ginger isn't a purebred), her birth date (a real `xsd:date`; `pets:birthDate` also accepts a bare `xsd:gYear` when only the approximate year is known, e.g. for an adopted/rescue pet), her current body weight (a `pets:BodyWeight` individual reusing CCO's decimal-value/measurement-unit pattern, the same reification style `pets:DosageAmount` already uses), her sex, and her spay/neuter status. `:Self persona:hasPet :Ginger` closes the loop from the Person side. Ginger's actual medical care and her day-to-day care & feeding instructions live in the nested Medical and Care & Feeding cells instead; this is a minimal, standalone identification.

#### Graph

```turtle
<!-- databook:id: alice-ginger-subject-graph -->
<!-- databook:graph: http://www.example.org/v4/graphs/graph-37#graph -->
@prefix : <http://www.example.org/v4#> .
@prefix persona: <http://mee.foundation/ontologies/persona#> .
@prefix pets: <http://mee.foundation/ontologies/pets#> .
@prefix cco: <https://w3id.org/cco-domains/cco/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

:Self rdf:type owl:NamedIndividual ,
               persona:Person .

:Ginger rdf:type owl:NamedIndividual ,
               pets:Pet ;
    rdfs:label "Ginger (Alice's cat)"@en ;

    pets:name "Ginger" ;
    pets:hasSpecies <http://purl.obolibrary.org/obo/NCBITaxon_9685> ;  # Felis catus (domestic cat)
    pets:hasBreed <http://purl.obolibrary.org/obo/VBO_0100262> ;  # Mixed Breed (Cat)
    pets:birthDate "2020-06-15"^^xsd:date ;
    pets:hasBodyWeight :Ginger_Weight ;
    pets:sex "Female" ;
    pets:isSpayedOrNeutered true .

:Ginger_Weight rdf:type owl:NamedIndividual ,
               pets:BodyWeight ;
    rdfs:comment "Ginger's weight at her most recent vet visit."@en ;
    cco:ont00001769 "9.5"^^xsd:decimal ;      # has decimal value
    cco:ont00001863 cco:ont00001728 .          # uses measurement unit → Pound Measurement Unit

:Self persona:hasPet :Ginger .
```
