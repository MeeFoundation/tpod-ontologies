# Cell DataBook File Format

A **cell DataBook** is the file that carries a cell's structured content. It is a
[DataBook](https://github.com/w3c-cg/holon/tree/main/architectures/databook) — a Markdown file with
YAML frontmatter, extension `.databook.md` — and it is what makes its folder a cell: a folder
holding exactly one cell DataBook is a cell, and a folder holding none is a plain filesystem folder,
not a cell at all, even when cells of its own sit further down. See
[Filesystem Persistence](app-behavior.md#filesystem-persistence) in app-behavior.md for how the app
persists a cell as a folder.

One cell DataBook carries three things:

- **document fields** — six YAML keys describing the file itself, above the `v4:` block;
- **the `v4:` block** — the cell's category, its creator and owners, its tags, and its links to the
  graphs below, whose keys map onto properties defined in `cell.ttl`. See
  [Cell Ontology](README.md#cell-ontology) in README.md for what each property *means*; this
  document says how each is *written*;
- **the body** — one `### Graph NN` section per graph the `v4:` block links, each holding that
  graph's own Turtle.

A graph has no file of its own: it lives inside the cell DataBook that links it, as one
`v4.member`/`v4.tool[].graph` entry plus one body section.

**Nothing in the file records where the cell sits.** There is no tree-position field, no parent
link, and no back-pointer from a graph to the cell that links it — a cell asserts `v4.member` and
`v4.tool`, and that is the only direction the link runs. A cell's position is simply wherever its
folder currently sits; a graph's containing cell is simply wherever its entry physically lives.
That is what makes moving or renaming a folder a pure filesystem operation with nothing in any file
to update, and what lets two members of a shared cell each file it wherever they like in their own
tree without touching content the other sees. It is also why two cells can never share a folder: a
file sitting in it would be ambiguously part of both.

**The rest of a cell's content is not in this file.** The DataBook holds the structured content and
the metadata about the cell itself; a cell's unstructured content sits beside it:

- **the note** — one Markdown file named after the folder (`X.md` inside the folder `X`), shown in
  the app's Note area. Naming it after its folder is the folder-note convention PKM tools such as
  Obsidian already use, which is what lets a cell tree double as a vault;
- **the attachments** — the plain files inside the folder's own `_cell-attachments` subfolder, flat,
  like email attachments. Every cell has that subfolder, empty or not, and its contents are the part
  of a cell's folder that travels when the cell is shared;
- **the member's own private files** — every other plain file loose in the folder, and any subfolder
  with no cell anywhere beneath it. These stay in that member's copy of the cell and never reach
  another member. The remaining two kinds of subfolder are not the cell's content at all: a
  descendant cell, holding its own DataBook, and a bare pass-through directory on the way to one
  (integrity.md's Check 11);
- **the chat** — a stream shared by the cell's members, not a file in the folder at all.

None of these is named or listed anywhere in the DataBook. There is no attachment manifest and
no note-filename field: the note is found by its name and the attachments by reading one reserved
folder, so adding a file to a cell is just putting a file in that cell's folder — and attaching it,
so that every member gets it, is just putting it in `_cell-attachments` instead — whether the app or
the user does it. `c:note`, `c:attachment` and `c:chat` are documentation-only properties — described in
README.md's [Documentation-only Properties](README.md#documentation-only-properties), declared in no
ontology, and never written as a triple by anything (integrity.md's Check 12).

This document specifies the DataBook file and nothing else; for how a cell's folder is laid out
around it, see [Filesystem Persistence](app-behavior.md#filesystem-persistence) in app-behavior.md.
For real files, see `example/Cells/` and [example.md](example.md).

## Why This Format

This is how the app persists a cell. Three properties are what make the format the right shape for
it.

**It is human-readable.** A cell DataBook is Markdown with YAML frontmatter, so a cell can be
navigated, inspected, and edited with ordinary tools rather than only through the app. Maintaining
this repo's own example tree in VS Code and Claude Code is the demonstration: everything the format
carries is legible as text, and anything wrong with it is visible in a diff.

**It blends into the user's existing files and folders.** A cell *is* a folder, and most of what it
holds is the ordinary files in it — the note and the attachments above, in the places a PKM tool
already looks for them. The result is that v4's storage is interoperable with a PKM vault rather
than parallel to it — Obsidian in particular. Running v4 alongside an existing
vault is a supported workflow, not a migration away from one: the two are built for different
requirements — a PKM tool for a single author's own knowledge, v4 for sharing cells with friends,
family, and groups — and adopting the second should not cost the user the first.

**It is machine-verifiable.** The format is constrained from three directions: SHACL shapes
validate a cell's synthesized triples, [integrity.md](integrity.md)'s checks cover what SHACL cannot
express, and [CLAUDE.md](CLAUDE.md) records the conventions behind both. Together they are a
diagnostic independent of the app — a second reading of the same rules, against which whatever
validation v4 implements internally can be checked. A single implementation has nothing to disagree
with.

The format will change, though. It has so far been exercised by one worked example and the
validation pipeline around it, not by an implementation, and the v4 implementation team will find
requirements it does not yet meet — a field that has to be added, a convention that holds across the
example tree but not across a real user's, a distinction that only matters once cells are syncing
between real instances. The largest known gap is tools: three of the four kinds have no data format
at all yet. See [Open Questions](#open-questions) at the end for that and the rest of what is
still unsettled. This document tracks the format as it stands rather than freezing it; what
keeps a proposed change honest is that [integrity.md](integrity.md)'s checks and the tree under
`example/Cells/` make its blast radius visible before it is made.

## Filename Convention

Cell-databook filenames follow (there is no separate category-databook file — a folder's sole
DataBook is its cell-databook, see [Cell/Category split](CLAUDE.md#key-architectural-patterns)):

```
<local>(<catType>).databook.md  — cell-databook
```

`<local>` is an **exact copy of the folder's own name** — verbatim, no kebab-casing, no lowercasing,
whatever case/spacing/punctuation the folder itself has (e.g. `Acme`, `Paula Walker`, `ATT`). There
is no `-cell` token: cell-databook is the sole DataBook type in a user's instance tree, so nothing
needs to be disambiguated by it. There is also no numeric disambiguator of any kind (no `-2`, `-N`,
etc.): a folder holds **at most one** cell-databook, ever — a folder is a **cell** only when it
holds exactly one such matching file, and a folder with no matching cell-databook is simply a plain
filesystem folder, not a cell at all. `<catType>` is the folder's own category classification,
kebab-cased (e.g. `Employees` → `employees`, `ImmediateFamily` → `immediate-family`, `SSN` → `ssn` —
kebab-casing is acronym-aware: a hyphen is inserted only at a lowercase→uppercase boundary or an
uppercase-run→lowercase boundary, so consecutive capitals stay together). If the matched category
concept's own local name carries a literal `(org)` disambiguator (used only to distinguish it from a
same-named Person-side sibling concept, e.g. `cat:BankingPayments` vs. `cat:BankingPayments(org)`),
that suffix is dropped before kebab-casing — `<catType>` only ever needs to disambiguate a
*recurring folder name* by role (e.g. were the same person to appear both as a leaf under
`Employees` and as one under `ImmediateFamily`, both Person-side), never the Person/Organization
split itself, which is already carried by the folder's own tree position and by `c:category`'s
actual asserted value, never by the filename. So a bank cell whose `c:category` is
`cat:BankingPayments` (Person-side, since it's the person's own relationship with the bank, not
company business filed under `Work`) is named `<local>(banking-payments).databook.md` with no `-org`
marker, and the same bare `banking-payments` `<catType>` would apply identically if a cell's
`c:category` were instead the org-side `cat:BankingPayments(org)`, since nothing in the filename
needs to tell the two apart.

A cell-databook's `<catType>` parenthetical is purely a filename-level disambiguator — `cat:catType`
does not exist in RDF at all, so nothing in RDF records it, and nothing reverse-matches the filename
to derive it. The one RDF-level echo of a folder's classification is `c:category`, read directly
from the cell-databook's own explicit `v4.category` field (see [The `v4` Block](#the-v4-block)), not
derived from the filename at all. Unlike the filename, a cell-databook's `id:` is deliberately *not*
derived from the folder name either — see [`id`](#cell-id) below.

**UserDefined folders — `<catType>` is the literal `custom`**: a cell may legally carry no
`c:category` at all — this is the UserDefined category, for a cell the user created without picking
any existing category concept. Since there is no category concept to kebab-case into `<catType>`,
the filename uses the fixed literal string `custom` in its place, e.g. a folder named `Friends` with
no category is `Friends(custom).databook.md`. The compression rule below still applies verbatim on
top of this (a folder literally named "Custom" would compress to `Custom.databook.md`, though no
real example does this) — `custom` is just an ordinary `<catType>` value from the filename's point
of view, it just happens to never come from kebab-casing a `skos:prefLabel`.

**Compression rule**: if `<local>`, normalized the same acronym-aware way `<catType>` already is, is
identical to the kebab-cased `<catType>`, the parenthetical is dropped entirely, since it's pure
redundancy — `<local>.databook.md` — rather than `<local>(<local>).databook.md`. For example
`cat:Work`'s folder is named `Work`, and its own `catType` (`Work`) also kebab-cases to `work` — the
same string — so its file is `Work.databook.md`, not `Work(work).databook.md`. This applies on a
normalized-equal match, not raw string identity (since `<local>` itself is never kebab-cased):
folder `Health & Wellness`'s catType `HealthWellness` both normalize to `health-wellness`, so it
compresses too, to `Health & Wellness.databook.md`. `Acme(organization).databook.md` keeps its
parenthetical since normalized `Acme` (`acme`) ≠ `organization`. Most of a tree's top-level scaffold
compresses this way, since these folders' own name simply *is* their category.
`Banking & Payments Firms(banking-payments).databook.md` is a further example of the
non-compressing case: normalized `Banking & Payments Firms` (`banking-payments-firms`) ≠
`banking-payments`, since the folder's own name matches `cat:BankingPayments`'s full
`skos:prefLabel` ("Banking & Payments Firms") rather than a shortened form.

Folder naming is standardized as the category's own display label (the OS folder name is used
verbatim, with no override field anywhere — the cell-databook's own `title:` field mirrors this name
exactly rather than overriding it, see integrity.md's Check 19), but a folder's own name alone can't
disambiguate a repeated name's *role* — the same person can legitimately appear at two different
tree positions, e.g. as a leaf under `Immediate Family` and again as a leaf under an employer's
`Employees`, both folders literally named after them — so `catType` carries that role encoding in
the filename instead, not derived from folder position. Such a pair never collides: one would be
`<name>(immediate-family).databook.md` and the other `<name>(employees).databook.md` (an employee
cell reuses the "Employees" scaffold's own category directly, the same "child folder reuses its
parent's category" pattern a pet's own cell under `Pets` already uses — there is no separate
narrower "Employee" category).

## Frontmatter

Every cell DataBook opens with the same six YAML fields, above its `v4:` block and in this order:
`id`, `title`, `type`, `version`, `created`, `description`. They describe the DataBook itself rather
than the cell's content — only `id` reaches RDF at all, and none of the six corresponds to a
property in `cell.ttl`. The cell's content proper is the `v4:` block below them, documented in
[The `v4` Block](#the-v4-block).

<a id="cell-id"></a>

### `id`

The cell's own id, and the RDF subject every triple synthesized from this DataBook hangs off —
`helpers/databook_graphs.py` reads it directly as the subject IRI of the `c:Cell` individual. It is
the one frontmatter field with ontology weight, and the one field a DataBook cannot omit. It is
deliberately *not* derived from the folder name or the filename (see
[Filename Convention](#filename-convention)): encoding a name into it would risk a collision the
moment two folders elsewhere in the tree shared both a name and a category, and nothing depends on
the id's string structure.

A cell's id is globally unique across every user's independent tree, not merely within one person's
own. It is flat and opaque, never derived from the cell's own name or category, and no registry or
central coordination assigns it — consistent with no cell, and nothing about it, ever being held by
a cloud provider or third party (see [Cell Storage](app-behavior.md#cell-storage)), and with
`:Self`'s purely-local identifier (see
[`:Self` IRI convention](CLAUDE.md#key-architectural-patterns)). Instead, it is derived from its
creator's identity and freshly generated random bytes (`‖` is byte concatenation):

```
nonce     = 16 random bytes
cell_id   = BLAKE3 derive_key("pdn/cell-id/v1", pdn_id ‖ announcement_pubkey ‖ nonce), first 16 bytes
signature = sign(announcement_secret, "pdn/cell-founding/v1" ‖ pdn_id ‖ announcement_pubkey ‖ nonce)
```

`pdn_id` is the creator's PDN ID; the announcement key pair belongs to their identity, shared by all
their devices, not to one device. The id is written as 32 lowercase hex characters. `pdn_id`,
`announcement_pubkey`, `nonce` and `signature` are stored in the cell's founding event — the first
event in the cell's membership store; the id itself is not stored.

A founding event is valid only when the id recomputed from its fields matches and its signature
verifies (see [Deriving and Checking a Cell Id](app-behavior.md#deriving-and-checking-a-cell-id)).
This is what prevents a member from feeding a device that already knows the id (from its identity's
records or a note link) a forged history with a different founder — a random id such as a v4 UUID
names no one and cannot. The context strings keep this hash and signature apart from any other made
over the same bytes; without the founding event, which only members hold, the id reveals neither
creator nor creation time.

This repo's own example data uses sequential `http://www.example.org/v4/cells/cell-<NN>` ids instead
(see integrity.md's Check 9) — the same flat, opaque shape, deliberately simple for one worked
example living entirely under a single shared example domain, and not unique once real cells belong
to many different users' independent instances.

### `title`

The cell's own name, and always exactly the name of the filesystem folder holding the DataBook —
verbatim, same case, spacing and punctuation. The folder is authoritative: renaming the folder means
updating `title:` to match, never the reverse, and `title:` is never an independent display-name
override (integrity.md's Check 19, which also treats it as authoritative for what a cell "is called"
when matching diagram box labels). It is shared, synced cell content, kept identical across every
member's copy, and any member may rename the cell — see
[Naming, Renaming, and Sharing](app-behavior.md#naming-renaming-and-sharing) in app-behavior.md for
the one exception, a bare two-member cell, whose name is instead independent per member.

### `type`

Always the literal `cell-databook` — the only DataBook type in a user's own instance tree, which is
what lets the folder ownership boundary rule identify a cell by the mere presence of a
`*.databook.md` file without needing any further marker. It is also the tooling's file filter: both
`helpers/yaml-to-rdf.py` and `helpers/validate.py` skip any DataBook whose `type` is anything else,
so a wrong value silently drops the cell from RDF synthesis and validation alike rather than
raising. No integrity check asserts the value.

### `version`

A hand-maintained [semantic version](https://semver.org/) for this one DataBook's own content. No
integrity check enforces it and the repo defines no bump rule, so it carries whatever meaning its
author gave it; in the example tree the values run from `1.0.0` to `2.2.0`, always with a zero patch
component. It is not synthesized into RDF. JSContact's `updated` property maps onto this field
rather than onto any ontology property — see the JSContact mapping table under
[Contact-Related Classes and Properties](README.md#contact-related-classes-and-properties) in
README.md.

### `created`

An unquoted ISO 8601 calendar date, `YYYY-MM-DD`, recording when the cell was created. Hand-entered:
no check reads it, nothing derives it from the filesystem or from git, and it is not synthesized
into RDF.

### `description`

A prose summary of the cell, written as a folded block scalar (`description: >`). Not used by any
tooling and not synthesized into RDF. Throughout the example tree it follows one house style: it
opens `Cell DataBook for folder "<title>" (cell:category: cat:<Concept>)`, optionally noting where
the cell is nested or whose category it reuses, then characterizes the cell's own shape — how many
members it has, and what its tool is about if it carries one.

## The `v4` Block

Below the six document fields sits a single `v4:` mapping carrying the cell's own content. Its
scalar-valued keys map one-for-one onto properties defined in `cell.ttl`:

| YAML field | Ontology property | Cardinality | Meaning |
|------------|-------------------|-------------|---------|
| `v4.category` | `c:category` | 0..1 | The category concept this cell was originally instantiated as — a `skos:Concept` individual in `cat:CategoryScheme` (e.g. `"cat:Others"`) or in a [category extension](README.md#category-extensions)'s own scheme (e.g. `"bhscat:BostonHubSociety"`); absent otherwise. Fixed at creation, not re-derived from the folder's current name. A hint for a recipient's app when this cell is shared with another member |
| `v4.creator` | `c:creator` | 1 | Who created this cell's content — a `p:Person` |
| `v4.owner` | `c:owner` | 1+ (required, no upper bound) | Which of the cell's members hold the owner role — always includes `v4.creator`'s own value; a `p:Person`, never an `s:Service` |
| `v4.userTag` | `c:userTag` | 0..N | A free-text tag the user minted (e.g. a pet's name, to gather every cell about that pet). Shared cell content |
| `v4.serviceTag` | `c:serviceTag` | 0..N | A tag written by this member's own service module for its own bookkeeping. Each entry is a mapping of three sub-keys — `namespace`, `key`, `value` (`c:tagNamespace`/`c:tagKey`/`c:tagValue`), e.g. `namespace: "foundation.mee.applecontacts"`, `key: "group"`, `value: "Christmas List"` — not a single string. Never displayed and never findable by the user — reachable only by the writing module, within its own namespace — and **local to this member's copy** — the one piece of cell content that does not propagate on a share |

Values are written as quoted CURIEs (`"cat:Pets"`) or bare local names (`":Self"`); both are
resolved to full IRIs by `helpers/databook_graphs.py`. **Any key whose cardinality allows more than
one value may be written either as a YAML list or, when it holds a single value, as a bare scalar** —
`owner: ":Self"` and a one-item list are equivalent, and the same latitude applies to `member`
below.

There is no *cell-level* `v4.subject` field — who or what a cell's content is about is derived from
`v4.member`/`v4.tool` rather than asserted independently (see integrity.md's Check 18); the
`subject:` key that does appear sits inside each `v4.member` entry, naming that member rather than
the cell's own subject.

The two remaining keys, `v4.member` and `v4.tool`, are link-valued: each entry names one graph
embedded in this same file's body. In ontology terms:

| Property | Value | Cardinality | Meaning |
|----------|-------|-------------|---------|
| `c:member` | `c:MemberGraph` | 1+ (required, no upper bound) | The required baseline of self-vs-other classified graphs backing this cell's content — one or more per member in the relationship — distinguished by each linked graph's own `c:subject`/`c:claimant` combination rather than by separate properties or classes |
| `c:tool` | `c:Tool` | 0..N — a cell with none is the ordinary case, and nothing caps how many it may carry (see [Tools](README.md#tools)) | Each tool brings its own data format and its own UI contribution; a form tool states, once, what its content is about (`c:formTopic`) |
| `c:formGraph` | `c:FormGraph` | 1+ (required) on a live `c:Form`, capped in practice at the cell's own member count, per tool (see integrity.md's Check 25) | The graphs beneath one tool, one per claiming member; a different range from `c:member`, since a tool's `c:formTopic` need not be a PDN-mappable identity |

Nothing in an entry marks its own kind. The list it sits in settles it: a `v4.member` entry is a
`c:MemberGraph`, a graph under a `v4.tool` entry is a `c:FormGraph`. The two are `owl:disjointWith`,
so neither ever carries the other's fields.

### `v4.member` Entries

One entry per member graph — at least one required, no upper bound. A single entry may be written as
a bare mapping rather than a one-item list. Sub-keys:

| Sub-key | Required | Value |
|---------|----------|-------|
| `id` | yes | The graph's full IRI — see [Graph Ids and Named Graphs](#graph-ids) |
| `claimant` | yes | Who is making the claim — see [`claimant` Vocabulary](#claimant-vocabulary) |
| `subject` | yes | The party whose member entry this graph is — see [`subject` / `formTopic` Vocabulary](#subject--formtopic-vocabulary) |
| `shape` | no | The `sh:NodeShape` CURIE the graph's content conforms to (`c:shape`), e.g. `"pshapes:ContactInfoShape"`. May itself be a list where one graph's content satisfies several shapes at once. A graph with no `shape:` is skipped by the template validation pass |

### `v4.tool` Entries

One entry per tool the cell carries; zero is the ordinary case. Always written as a list. Sub-keys:

| Sub-key | Required | Value |
|---------|----------|-------|
| `type` | yes | Which tool class this is: `form`, `calendar`, `canvas` or `map`, mapping to `c:Form`/`c:Calendar`/`c:Canvas`/`c:Map`. Only `form` has a content model today, and only `form` appears in the example tree |
| `formTopic` | yes on a form | What the tool's content is about (`c:formTopic`) — any resource IRI, stated once by the tool rather than repeated on each graph beneath it |
| `graph` | yes on a form | A list of that tool's own graph entries, at least one |

Each entry in `graph:` carries `id`, `claimant`, and optionally `shape`, exactly as a `v4.member`
entry does — but **never `subject`**: a tool graph's about-ness lives one level up, on the tool's
single `formTopic`.

<a id="graph-ids"></a>

## Graph Ids and Named Graphs

A graph lives physically inside its owning cell-databook's `v4.member`/`v4.tool[].graph` entries and
body (see [Cell/Category split](CLAUDE.md#key-architectural-patterns)) — it has no file or
filename of its own. Each entry's own `id` (which doubles as the graph's
own named-graph identity, `{id}#graph`) does not re-encode `claimant`/what the graph is about/the
containing cell into the id string, since those facts are already carried by that same entry's own
sibling `claimant:` and `subject:` fields, or its tool's `formTopic:`, and the containing cell is
simply wherever the entry physically lives — encoding them a second time would be pure redundancy.
It follows a single flat pattern instead:

```
http://www.example.org/v4/graphs/graph-<NN>
```

`<NN>` is the same graph number used everywhere else for this graph — the diagram label, the
`### Graph NN` body heading, and its `<a id="graph-NN">` anchor. It is zero-padded to two digits up
to `graph-99`, and runs on into three digits from `graph-100` — the numbers are minted in one flat
sequence with no leading zero beyond that padding, so `graph-09` and `graph-100` are both
well-formed while `graph-009` is not. A `v4.member`/`v4.tool[].graph` entry carries this full IRI
directly as its own `id` field — there's no separate list to cross-reference it against.

**DataBook IRI convention**: a document's `id:` and its `graph.named_graph:` always differ by the
`#graph` fragment — `named_graph` is always `{id}#graph`. The `databook:id` on a block is a fragment
identifier making that block independently addressable as `{id}#{block-id}`.

### `:Self` and Locally-Minted IRIs

The three about-ness and attribution fields below all hold individual IRIs, minted by one
convention. The user's own `p:Person` individual always uses the IRI `:Self`, in every graph in
their own instance. Everyone else — other people, organizations, groups, services — gets a
locally-minted named IRI (`:Bob_Johnson`, `:Acme`).

`:Self` is local and is never exposed over the PDN, so two instances of the app never collide on it:
in each instance it names that instance's own user, and nothing has to reconcile the two. A graph
that arrives from a peer, where that peer was `:Self` in their own instance, is rewritten on receipt
so `:Self` still means the receiving user; the peer is assigned a locally-minted identifier of the
receiver's own, which resolves to or is replaced by their PDN ID once a connection is established.

This is why the example tree can be read as one user's instance throughout even though some of its
graphs were authored by other people: `:Self` is Alice's everywhere in it, whoever wrote the claim.

### `claimant` Vocabulary

A `v4.member`/`v4.tool[].graph` entry's own `claimant:` field takes the local IRI of a `p:Person`,
`o:Organization`, or `s:Service` individual. Which of the three a graph names turns on who is
*really* making the claim, not on which member mechanically carries it. Specifically: `:Self` (the
user's `p:Person`) for self-claimed graphs; a named `p:Person` individual when another user claims
the data; a named `o:Organization` individual for content contributed by a `s:ServiceProvider` that
organization provides, since the organization is the responsible party and the one an eventual
cryptographic signature would name; and a named `s:Service` individual for a service with no
organization standing behind it in the relationship. Note that an organization claimant need not be
a member subject — it is reached from one via `s:providedBy`, which is what integrity.md's Check 25
allows for.

**"Other" claimants**: When the claimant is someone other than the current user (`:Self`), the
claimant is a named individual of one of:

- `p:Person` — another user (a different person claiming data about the user)
- `o:Organization` — a company, nonprofit, or government agency that is a PDN node, claiming on
  behalf of the `s:ServiceProvider` it provides
- `s:Service` — a service claiming under its own IRI, with no organization behind it in the
  relationship (e.g. an invited agent service, or a cell backup service)

An organization only ever appears as a claimant when it is PDN-interoperable. Where it is not, the
user self-enters that data and the claimant is `:Self`. (This distinction is currently a
data-modeling convention, not something any property formally enforces.)

### `subject` / `formTopic` Vocabulary

Which of the two about-ness fields applies is settled entirely by the list the entry sits in — a
`v4.member` entry is a `c:MemberGraph` and carries `subject:` (the party whose member entry it is,
always a PDN-mappable identity), a graph under a `v4.tool` entry is a `c:FormGraph` and carries no
about-ness field of its own — its topic is the holding tool's single `formTopic:` (what the content
is about, which need not be a PDN identity at all). Neither kind ever carries the other's field. See
`cell.ttl`, and [Graphs](README.md#graphs) in README.md, for why the two are separate properties on
separate disjoint classes.

**Examples** (id local-name, which list it sits in, and the corresponding field values found in that
same `v4.member`/`v4.tool[].graph` entry), drawn from the worked example in
[example.md](example.md):

| Id local-name | List | About (`subject`/`formTopic`) | Claimed by | Containing cell |
|----------|------|---------|-------------|---------------------|
| `graph-76` | `tool` | Self (Alice) | Citibank | Citibank(banking-payments) |
| `graph-07` | `tool` | Sophia Walker | Self (Alice) | Sophia Walker(immediate-family) |
| `graph-92` | `tool` | BHS | BHS | Boston Hub Society |
| `graph-08` | `member` | Self (Alice) | Bob Johnson | Bob Johnson(others) |
| `graph-03` | `member` | Bob Johnson | Bob Johnson | Boston Hub Society |
| `graph-01` | `member` | BHS's service | BHS | Boston Hub Society |

<a id="body"></a>

## Body Structure

Below the closing `---` of the frontmatter, the body holds one section per graph the `v4:` block
links — every graph, whether it came from `v4.member` or from a `v4.tool`'s own `graph:` list, in
one flat sequence under a single `## Graphs` heading. Nothing in the body says which list a graph
came from; the frontmatter already settled that.

Each graph contributes exactly four things, in this order:

1. **An HTML anchor** — `<a id="graph-NN"></a>`, making the section linkable as
   `<file>.databook.md#graph-NN`. example.md's tables link every graph this way.
2. **A `### Graph NN` heading**, with the same `NN` as the anchor and as the entry's own `id`.
3. **A `#### Overview` subsection** — prose saying what the graph holds and why. By convention these
   open "This graph captures…".
4. **A `#### Graph` subsection** holding a single fenced ```` ```turtle ```` block: the graph's
   content.

The fence opens with two HTML-comment marker lines before any prefix declaration:

```
<!-- databook:id: <human-readable-slug> -->
<!-- databook:graph: http://www.example.org/v4/graphs/graph-NN#graph -->
```

`databook:graph:` is the `{id}#graph` named-graph IRI, and it is the marker the tooling actually
reads — `helpers/databook_graphs.py` isolates one graph's fence in a multi-graph file by matching
it. `databook:id:` is a human-readable slug making the block independently addressable; no script
reads it. Both marker lines are stripped from the extracted Turtle.

### Self-Containment

Every graph is self-contained: it carries everything needed to read it, and borrows nothing from any
other graph. Concretely, a graph re-asserts the bare `rdf:type` of every named individual it
references — `:Self rdf:type owl:NamedIndividual, p:Person` appears in each of the graphs that
mention `:Self`, not once in some shared file the others merge in, and the same holds for every other
named individual.

The repeated type declarations look redundant and are not. A graph is the unit that gets extracted,
validated, signed, and shared: one graph's Turtle pulled out on its own has to be complete RDF that
validates against its shape without the rest of the tree present. Nothing else in the format
guarantees that, and a single borrowed declaration would break it silently — the graph would validate
in a merged dataset and fail alone.

There is no separate file holding a user's identity data, and no exception for a named individual's
own type declaration. Every substantive fact lives in the graph it belongs to.

## Skeleton

A complete, minimal cell DataBook — one member entry and one form tool with one graph:

````markdown
---
id: http://www.example.org/v4/cells/cell-NN
title: "Folder Name"
type: cell-databook
version: 1.0.0
created: 2026-01-31
description: >
  Cell DataBook for folder "Folder Name" (cell:category: cat:Concept). One-member cell with
  one member entry about :Self and one tool graph about :Topic.
v4:
  category: "cat:Concept"
  creator: ":Self"
  owner: ":Self"
  userTag:
    - "a tag"
  member:
    - id: "http://www.example.org/v4/graphs/graph-NN"
      claimant: ":Self"
      subject: ":Self"
      shape: "pshapes:ContactInfoShape"
  tool:
    - type: "form"
      formTopic: ":Topic"
      graph:
        - id: "http://www.example.org/v4/graphs/graph-MM"
          claimant: ":Self"
          shape: "someshapes:SomeShape"
---

## Graphs

<a id="graph-NN"></a>
### Graph NN

#### Overview

This graph captures …

#### Graph

```turtle
<!-- databook:id: some-member-graph -->
<!-- databook:graph: http://www.example.org/v4/graphs/graph-NN#graph -->
@prefix : <http://www.example.org/v4#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix persona: <http://mee.foundation/ontologies/persona#> .

:Self rdf:type owl:NamedIndividual ,
               persona:Person .
```

<a id="graph-MM"></a>
### Graph MM

#### Overview

This graph captures …

#### Graph

```turtle
<!-- databook:id: some-tool-graph -->
<!-- databook:graph: http://www.example.org/v4/graphs/graph-MM#graph -->
…
```
````

## What Validates This

No single tool checks the whole format. It is enforced in three places:

- **[integrity.md](integrity.md)** — Check 1 (every graph has both an entry and a body section),
  Check 2 (`graph-<NN>` id pattern), Check 3 (entry well-formedness: which sub-keys each kind of
  entry carries), Check 9 (`cell-<NN>` id pattern), Check 11 (folder ↔ cell-databook structure),
  Check 19 (`title:` matches the folder's OS name), Checks 26/27 (a `shape:` value against the
  graph's own content, and against the cell's category's own template), and Check 36
  (`v4.userTag`/`v4.serviceTag` well-formedness).
- **`helpers/validate.py`** — synthesizes `c:` triples from the frontmatter and runs SHACL
  (`shacl/cell-shacl.ttl` and friends) against them, plus a per-graph template pass driven by each
  entry's `shape:` value. See [Validation](example.md#validation) in example.md for the commands.
- **`helpers/databook_graphs.py`** — the parser, and the de facto machine-readable spec for which
  keys are actually consumed. It reads exactly: top-level `id` and `type`;
  `v4.category`, `v4.creator`, `v4.owner`, `v4.userTag`, `v4.serviceTag[].{namespace,key,value}`;
  `v4.member[].{id,claimant,subject,shape}`; and
  `v4.tool[].{type,formTopic,graph[].{id,claimant,shape}}`. No other key is consumed anywhere; an
  unrecognized key is silently ignored.

## Open Questions

What this format does not settle. Each is a change to this document when it is settled, and each is
listed because a reader hitting it should be able to tell that it is genuinely open rather than an
omission.

### Where chat content goes

Every cell has one chat stream, always — `c:chat`, 1..1, present even when empty — and nothing
anywhere says where it is stored. It is not in the DataBook, and unlike the note and the attachments
it has no place in the folder either: it is the one piece of a cell's content with no specified
storage at all. It is also the piece least like the others. A note is one document that is rewritten;
a chat is append-only, authored per message, potentially far larger, and read at its tail far more
often than in full.

Two constraints narrow the answer. Dropping a transcript into the cell's folder as a plain file makes
it one of the member's own private files, or an attachment if it goes in `_cell-attachments`, unless
something says otherwise — and either way puts it in the user's PKM vault, which may be a feature
or a mess, but is not currently a choice anyone has made. And a private 1:1 thread between
a member and their own agent is not visible to other members
(see [Chat Area](app-behavior.md#chat-area) in app-behavior.md), so it cannot live in shared, synced
cell content the way the group stream can — whatever holds a cell's chat has to hold at least two
things with different propagation rules. A cell already has one piece of content that does not
propagate on a share, `c:serviceTag`, so the precedent exists; what is new is that here the split
runs *within* one feature rather than between two properties.

### Where a non-form tool's content goes

Only `c:Form` has a data format today. Its content is graphs, and a graph is Turtle, which is why
every one of the 101 fences across this repo's example tree is a ```` ```turtle ```` one.
`c:Calendar`, `c:Canvas` and `c:Map` are declared with no content model at all, so this document has
nothing to say about what a calendar's entries or a canvas's drawing surface look like on disk.

Settling any of them lands in two places: a `v4.tool` entry needs whatever keys that kind's data
calls for alongside `type`, and the body needs somewhere to put the content.
`formTopic`/`formGraph` are scoped to `c:Form` precisely so a kind with a different shape is not
forced through them. A calendar's entries are plausibly still graphs, and so still Turtle; a canvas's
drawing surface is plausibly not, which runs into the next question.

### Where a tool's binary content goes

A drawing surface, a scanned document, a map's cached tiles — some of what a tool holds will not be
text. It belongs in **its own file in the cell's folder, referenced from the graph**, not encoded
into a body section. The example tree already works this way for the one binary-ish thing it
carries: a passport photo and a driver's license photo, each an `xsd:anyURI` value on `p:hasPhoto`
rather than image data. Git, a diff, and the sync layer all get to treat a PNG as a PNG.

Putting it in the DataBook instead spends most of what recommends this format in the first place.
There are two ways to try, and the objection to both is the same:

- **Base64 inside the Turtle**, as an `xsd:base64Binary` literal, is legal RDF and needs no format
  change at all. But a megabyte of drawing becomes a single unbreakable line a third larger than the
  original — no longer readable as text, no longer diffable, and rewritten whole in git on every
  stroke.
- **A separate fenced block** tagged as something other than `turtle` carries the same size cost,
  and adds one of its own: `helpers/databook_graphs.py` matches the literal ```` ```turtle ````
  opener, so a differently tagged fence is passed over rather than rejected. Content put in one
  today is silently invisible to every tool in this repo rather than failing loudly.

Either could still be right for something small and genuinely inseparable from the claim carrying it
— a signature, a thumbnail — but not for a tool's working data, and the threshold at which "small"
stops applying is itself unset.

What stays open is the reference rather than the storage. A relative path is the obvious thing for a
graph to hold, but a graph is claim content that propagates between members on a share, so whatever
it holds has to still resolve in a recipient's own copy of the cell — after the folder has been
renamed, renested, or received under a collision-suffixed name (see
[Naming, Renaming, and Sharing](app-behavior.md#naming-renaming-and-sharing) in app-behavior.md).
A path relative to the cell's own folder survives all three; anything anchored higher does not.

### How a tool's own files are told apart from the user's

This follows directly from preferring option 1 above. Every plain file sitting in a cell's folder is
already one of two things — an **attachment**, if it sits in `_cell-attachments`, or one of the
member's own private files if it sits loose — and both are shown to the user in the Attachments
area. That is the whole definition, and it is what makes adding a file to a cell as simple as putting
a file in its folder. But a canvas's backing image is not something the user attached, nor something
they chose to keep back, and showing it in either set alongside the files they did misrepresents
both. Telling them apart needs a rule the format does not have: a reserved filename prefix, a second
reserved subdirectory beside `_cell-attachments`, or an explicit manifest — the last of which would
cost the property that adding a file requires no DataBook edit. `_cell-attachments` is a precedent
for the second, being exactly a subdirectory that is neither a descendant cell nor a pass-through,
but it does not settle the question: a tool's own files are neither the cell's attachments nor the
member's private files, so a third disposition is still needed.
