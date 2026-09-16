# App Behavior

This file continues [README.md](README.md) and [example.md](example.md), which describe the Category, Cell, Graph, Persona, Organization, and Service ontologies and illustrate them with a worked example. This file documents how the app behaves *on top of* that data — cell lifecycle, storage, sharing, permissions, naming/renaming, what actions a user can take on a cell, what happens when a shared cell arrives somewhere new, and so on.

Nothing in this file changes any `.ttl` file or DataBook triple — every rule here is app-level behavior, not an ontology rule. This file is also written at the **user level** throughout: it describes what a member can do and sees in the app, not how the PDN layer beneath implements it. The two can legitimately differ, and where they do this file follows the user's view — see [Tool & Member Info Permissions](#tool--member-info-permissions) for the case where they diverge most visibly.

## Cell Storage

Cells are stored on the user's device(s) or, for an organization's own `s:ServiceProvider`, on Personal Data Network (PDN) nodes hosted by that organization. **A cell is never persisted in the user's filesystem**: its entire content lives in a protected, app-managed store, encrypted at rest — see [storage.md](storage.md) for that decision and the reasoning behind it. No cell is ever stored by any cloud provider, or any third party of any kind, including The Mee Foundation. When a cell is shared, changes to its contents — including its own name, for a single-member cell or a cell with three or more members, or a two-member cell that also carries a tool — propagate to every member over the PDN; see [Naming, Renaming, and Sharing](#naming-renaming-and-sharing) below for what stays independent per member instead. Two pieces of a cell's content never propagate at all: a member's own **private files**, as against the **attachments** every member receives (see [Cell Contents](#cell-contents) below), and a `c:serviceTag`, written by one member's own service module and meaningful only in the instance that wrote it (see [Tags](README.md#tags) in README.md). The two differ in who decides: the first is the member's own choice about a file of theirs, the second a bookkeeping label they never see.

### Cell Contents

A cell is a unit the app manages, identified by its own stable id (see [Deriving and Checking a Cell Id](#deriving-and-checking-a-cell-id) below). Nothing marks it in a filesystem, because it is not in one, and it carries no record of its own position in the tree: a cell's parent is per-member state in that member's own store, never shared content, which is what lets two members of a shared cell each file it wherever they like without touching what the other sees.

A cell may carry a `c:category` value. When present, it records the category concept — a `skos:Concept`, always ultimately reachable from `cat:Person` or `cat:Organization` — the cell was originally instantiated from; that concept is normally one of `cat:CategoryScheme`'s own, reached by following `skos:broader` upward, but it may instead belong to a [category extension](README.md#category-extensions)'s own scheme, in which case the path runs through that concept's single `skos:broadMatch` into the core taxonomy first and then upward by `skos:broader` as usual (`bhscat:BostonHubSociety` → `cat:Groups` → `cat:Person`) — so the three category types below are well-defined either way; this value is fixed at that point and never re-derived from the cell's current name or position, so neither needs to stay in step with it. There are accordingly **three category types**: **Person** (category reachable from `cat:Person`), **Organization** (category reachable from `cat:Organization`), and **Custom** (no `c:category` at all — a cell the user created without picking any existing category concept). Custom is identified precisely, not by judgment call: the cell simply carries no `c:category` value.

A cell's own **name** is a separate, purely display-level choice, independent of the above: when the cell does have a category, the name may be copied verbatim from that category's own `skos:prefLabel` (e.g. a cell named "Others" whose category is `cat:Others`), or the user may give it a different name entirely (e.g. a cell named "Bob Johnson" whose category is still `cat:Others`). The app's own record of the name is authoritative outright, and there is no independent display-name override anywhere. For a single-member cell or a cell with three or more members — or a two-member cell that also carries a tool — this name is part of the cell's own shared content: it is kept in sync and identical across every member's copy, exactly like its graphs, its attachments, its note (a note's own text, including any links it contains, but not necessarily the resolvability of a link pointing outside the cell — see the note description below), chat, `c:category`, and everything else the cell carries (see [Introduction to Cells](README.md#introduction-to-cells) in README.md). What stays independent per member is only their own tree *position* for the cell — the parent it's nested under, and so that parent's own name. A bare two-member cell (carrying no tool) is the one exception: there, the name itself is also independent per member, alongside tree position, rather than shared — see [Naming, Renaming, and Sharing](#naming-renaming-and-sharing) below for both this exception and how the app keeps a shared name unique within each member's own tree.

- A cell's **attachments** are the files every member of the cell receives, shown in the app's **Attachments area**, and they are what travels with the cell when it's shared. Attachments are flat, like email attachments. A file the member adds to the cell without attaching it is instead their own **private** file — it stays in their copy of the cell, syncs across their own devices like the rest of it, and never reaches another member. Both sets are shown in this same area: the attachments plainly, and the private files badged (🔒) under their own divider, keeping whatever structure the member has given them rather than being flattened in alongside the attachments. A file is attached or made private by dragging it across, and a member may hold private files in a cell that has no attachments at all. The distinction is about propagation and nothing else, so it is real even in the ordinary case of a single-member cell that shares nothing: it records what *would* travel if the cell were ever shared later — which is exactly the moment a wrong default would bite. Private content may be organized however the member likes; the flatness above is about what travels, and nothing that stays put needs it.
- A cell's **note** is shown in the app's Note area. A cell has exactly one, never more, written in Markdown, and it supports the same freeform linking PKM (Personal Knowledge Management) tools do: a note may link to any other cell's note anywhere in the user's tree, not just within its own cell. Once a link's target has actually been instantiated as a cell (see [Wikilink-Triggered Cell Creation](#wikilink-triggered-cell-creation) below for the one case where it hasn't been yet), the link resolves by that target cell's own stable, globally unique id (see [Cell Id](cell-databook.md#cell-id)) — not by matching its display text. Concretely, a resolved link is written using the alias syntax those same tools already support — `[[7f3a9c2e5d41b08f…|foo]]`, id before the pipe, display text after — rather than inventing new syntax; an unresolved link with no target yet (see below) is simply `[[foo]]`, no pipe at all. A link's own display text travels with the cell's note when the cell is shared, but resolution never falls back to text-matching. This matters because cell names are only unique among siblings, not globally (see [Naming, Renaming, and Sharing](#naming-renaming-and-sharing) below) — a recipient's own tree can easily contain an unrelated cell that happens to share a display name with the intended target, and id-based resolution is what keeps a link from ever silently jumping to that wrong cell instead. What id-based resolution can't fix is the linked-to cell itself not traveling with the note: if the target lies outside this cell's own boundary (i.e. it isn't part of this cell's own Attachments-area content or its own note) and the recipient doesn't independently have a cell carrying that id — because it was never shared with them, or they organize their tree completely differently — the link simply won't resolve on their side; it fails closed (inert, shown as unresolved) rather than open (silently pointing somewhere else). This is an accepted limitation of cross-cell linking, not a defect. That boundary has an inner edge as well: a link whose target is one of the member's own private files resolves in their own copy and fails closed on every other member's side, since a private file never travels — the same inert-rather-than-wrong behavior, for the same reason.

### Scaffolding: This Repo's Filesystem Tree

None of the above is a filesystem. The app does not exist yet, though, so this repository carries its worked example on disk, as a tree of folders under `example/Cells/`: one folder per cell, marked as a cell by a reserved `_cell-attachments` folder directly inside it, holding that cell's structured content as a `.databook.md` file, its note as a Markdown file named after the folder, its attachments inside the reserved folder, and the member's own private files loose beside them. **All of that is development scaffolding** — a way to carry, validate and diagram real cell content before there is an app to hold it — and none of it is a commitment about how v4 stores anything. It is specified in [Development Scaffolding](cell-databook.md#development-scaffolding) in cell-databook.md, which is the file to read wherever this repo's layout and the model above appear to disagree; [storage.md](storage.md) draws the boundary between the two.

<p align="center"><img src="images/folder-mapping.png" alt="This repo's scaffolding tree: each cell a folder holding its cell DataBook, its note file, its _cell-attachments folder, and the member's own private files"></p>

The diagram shows a slice of that tree — the `People` cell, its `Others` child, and `Others`' own `Fred Flintstone` child — with the folder-icon fill and folder-name text colors this repo's own diagrams use throughout: fill by category type (tan for Person, light blue for Organization, purple for Custom), and folder-name text **green** when the name matches the category's label verbatim, plain **black** when the user has customized it. A Custom cell's name has no label to possibly match, so it is always black text too, never green. The two colors are independent — a cell can be tan-filled with black text ("Fred Flintstone"), light-blue-filled with black text, or purple-filled with black text. Only a folder that is a cell carries fill at all; `_cell-attachments` and the private `A` folder stay white. In this repo's scaffolding a Custom cell's DataBook filename also carries the literal `(custom)` disambiguator in place of a category-derived `<catType>` (e.g. `Friends(custom).databook.md` — see the [Filename Convention](cell-databook.md#filename-convention) in cell-databook.md), and the two must agree; that filename is a scaffolding convention, never the test itself, which is the absence of `c:category` alone. The cell's name is likewise carried in the DataBook's `title:` field, which mirrors the folder verbatim (integrity.md's YAML-5).

### Deriving and Checking a Cell Id

The creating device derives a new cell's id (see [Cell Id](cell-databook.md#cell-id)) at the moment of creation and writes the cell's founding event. Every member device checks the founding event when it arrives, a newly linked device's first sync included: it recomputes the id, verifies the signature, and drops the event on any mismatch.

## Cell Management

This section is about how the app manages a **cell** specifically — its lifecycle, membership, permissions, naming, and what happens when one is shared.

### Lazy Instantiation

Cells for most category concepts are not pre-created ahead of time. A cell is not created until the user wants one. When a cell matching a templated concept (one for which some `c:TemplateCell` carries a matching `c:category` value) is first created, the app clones that `c:TemplateCell` into the new cell — real content later filed under it is validated against that template's own `c:memberShape`, or against the `c:formShape` of a tool it declares, found by the same `c:category` match rather than copied onto the new cell (content filed as a `c:member` graph is validated against `c:memberShape`, content held by a tool against that tool's `c:formShape` instead) — and the clone is given real member-classified content — typed `c:InstanceCell` — rather than staying purely a template. If the template declares any tool via `c:declaresTool` (18 of the 106 templates do, e.g. `cat:MedicalAppointment`'s, `cat:PetsMedical`'s, `cat:Companies`'s, and `cat:Home`'s — plus 3 more, e.g. `cat:HealthWellness`'s, whose tool holds a bare third-party-reference label rather than a specific document type), the clone is created carrying one live `c:tool` per declared tool, since a real cell of that category always ends up holding that content beyond its own `c:member` baseline.

If the user instead creates a cell with **no category** selected at all (the Custom/UserDefined case, identified by the cell carrying no `c:category` value at all), there is no `c:category` value to drive the usual reverse lookup, so this one case falls back to a different, fixed template instead: `ctpl:UserDefinedTemplateCell` (`cat-templates.ttl`) — the one `c:TemplateCell` carrying no `c:category` value at all, found as that unique category-less template rather than by matching a category. It carries only `c:memberShape pshapes:ContactInfoShape` and declares no tool — a Custom cell has no document type and no tool of its own, only ever a contact-info view of its member(s).

When a member then actually fills in that cell's `c:member` graph or a tool's own graph, the app also stamps the new graph's own `c:shape` value from that same lookup, using whichever of the two shape properties matches the list the new graph belongs to — the cell's `c:category` → its `c:TemplateCell` → that template's `c:memberShape` (for a `c:member` graph) or its declared tool's `c:formShape` (for a tool's own graph) → that shape's own CURIE, copied directly, since `c:shape`'s range is `sh:NodeShape` (`cell.ttl`), the same range `c:memberShape` and `c:formShape` already carry — there is no separate label to resolve. **This mapping is unconditional**: whenever a `c:TemplateCell` of category X carries a `c:memberShape` value, every real cell of category X must have its `c:member` graph(s) carry the matching `c:shape` value too, with no exception for which shape it happens to be. For example, a `cat:Passport` cell's sole tool graph → `ctpl:PassportTemplateCell` → its declared tool's `c:formShape idocshapes:PassportShape` → the graph's own `c:shape` is stamped `idocshapes:PassportShape` directly — integrity.md's TTL-3 separately verifies that shape's own `sh:targetClass` (`idoc:Passport`) is asserted via `rdf:type` on the graph's own new document individual; TTL-4 verifies the `template:` value itself against the cell's `TemplateCell`. Every one of the 106 templates in `cat-templates.ttl` uses `pshapes:ContactInfoShape` as its own `c:memberShape` (a `c:member` graph is always validated as a basic contact-info profile, regardless of category, while any category-specific content lives in a tool instead), so every real `c:member` graph's `c:shape` is likewise stamped `pshapes:ContactInfoShape` uniformly — even though that shape's own `sh:targetClass` is the broad `persona:Person` rather than a narrow reified document class, since it validates the graph's own subject individual in place rather than a separate reified document (integrity.md's TTL-3 carves this one shape out as its sole exemption from the rdf:type-matching rule, since a `c:member` stub graph legitimately need carry no `persona:Person` individual at all — e.g. an organization's own self-claimed member stub). Every `category.ttl` concept, the two SKOS top concepts `cat:Person`/`cat:Organization` included, now has a matching `c:TemplateCell` (integrity.md's TTL-6 — no real cell is ever categorized as bare Person/Organization), so the reverse `c:category` → `c:TemplateCell` → `c:memberShape` lookup above covers every real `c:member` graph without exception, including Alice's own contact info (`cat:Employees` → `ctpl:EmployeesTemplateCell`) — there is no longer a live case of a ContactInfo graph created with no cell-level template lookup at all.

### Number of Members

A cell can have just one member (the user) or several. We don't yet know how many members a cell can support, but the number is almost surely well under 100. An invited agent service (`s:AgentService`, see [Inviting AI Agents](#inviting-ai-agents) below) is a real member too, and counts toward this same tally — inviting one raises a single-member cell to a two-member cell, exactly as inviting a human would.

### Permissions

Cell-level capabilities are governed by two independent axes: **ownership** (`c:owner`, cell.ttl — owner vs. regular member) and **identity type** (human or service). A cell's creator (`c:creator`) is always its initial, and until any promotion its sole, owner; any current owner may promote any other current regular member of `p:Person` identity — never an `s:Service`, which can never hold the owner role, mirroring `c:creator`'s own person-only range — to owner, at which point that member's capabilities change as shown below. Any current owner may likewise demote another owner back to regular-member status, so ownership is not permanent once granted — the one limit being that a cell always retains at least one owner (`c:owner` carries `sh:minCount 1`), so the last remaining owner cannot be demoted. A single-member cell has only its creator, who is trivially its sole owner — the owner/regular-member distinction only becomes observable once a cell gains a second member. There is no separate guest tier — every member, of any identity type, has exactly the same access as any other member of the same ownership status.

Capabilities are grouped by the surface they govern, one table each: the **cell container** itself, its **attachments**, its **note**, and its **tool & member info** (graph claims). A capability appears in exactly one table.

We define three kinds of members:

- **Owner** — a user who is currently holding the owner role. The cell creator immediately becomes the cell's first, and initially sole, owner.
- **Member** — a user who is not currently an owner.
- **Service** — a service, (always a non-owner).

Every cell in every table now carries a decided value. A cell reading `n/a` marks a capability that genuinely cannot apply to that role, rather than one left open — an `s:Service` can invite no one, so it can never have a self-invited member to remove.

#### Cell Container Permissions

| Capability | Owner | Member | Service | Open Issue |
|---|---|---|---|---|
| Create cell | yes | yes | no |  |
| Invite member to a cell | yes | yes | no |  |
| Uninvite self-invited member | yes | yes | n/a |  |
| Remove member from cell | yes | no | no |  |
| Remove owner-member from cell | yes | no | no |  |
| Leave cell | yes | yes | yes |  |
| Rename cell for all members | yes | yes / no  | no |  #1 |
| Delete cell locally | yes | yes | yes |  |
| Delete cell for all members | yes | no | no |  #2 |
| Promote member to owner | yes | no | no |  |
| Demote owner to member | yes | no | no |  |
| Out-of-cell communications | yes | yes | no |  |

**Open Issues**

1. **Rename** — may any member rename a cell for everyone, or only an owner? This document's [Naming, Renaming, and Sharing](#naming-renaming-and-sharing) section argues at length for any member, against the Microsoft Teams/Discord/GitHub precedent; Vladimir and Sergey restrict it to owners.
2. **Leave vs. delete locally** — does *Leave cell* subsume *Delete cell locally*, or are they distinct? Leaving withdraws one's membership, which propagates; deleting locally removes the cell from one's own tree only. They are kept as separate rows pending an answer.

**Capabilities**

- **Create cell** — create a new cell in one's own tree. Only a human can: `c:creator`'s range is `p:Person` alone, so no service — provider, agent, or backup — can originate a cell, and none can invite anyone into one either. An organization's relationship with a person therefore only ever exists because the person created the cell and invited that organization's `s:ServiceProvider` into it; the organization cannot open the conversation.
- **Invite member to a cell** — invite a person, or a service (one's own AI agent, a backup service, or an organization's own service), to a cell of which one is already a member.
- **Uninvite self-invited member** — remove a cell member whom this member originally invited.
- **Remove member from cell** — remove any regular (non-owner) member.
- **Remove owner-member from cell** — remove a member who currently holds the owner role, as distinct from removing a regular member.
- **Leave cell** — withdraw one's own membership, dropping oneself from `c:member` (and from `c:owner`, if held). Its relationship to *Delete cell locally* is unsettled.
- **Rename cell for all members** — change the cell's shared name so the change propagates to every member's copy. See [Naming, Renaming, and Sharing](#naming-renaming-and-sharing) below for the full rule, including the bare two-member-cell exception where the name is independent per member rather than shared.
- **Delete cell locally** — remove the cell from this member's own tree only, not from any other member's copy.
- **Delete cell for all members** — only the owner can do this. 
- **Promote member to owner** — add a current regular member (a `p:Person`, never an `s:Service`) to `c:owner`.
- **Demote owner to member** — remove a current owner from `c:owner`, returning them to regular-member status. Restricted to owners, and never applicable to the cell's last remaining owner, since `c:owner` requires at least one value.
- **Out-of-cell communications** — communicate with another cell member outside the cell, by email or SMS, using contact information about that member that they have put in the cell.

#### Attachment Permissions

An attachment is a file every member of the cell receives, shown in the app's Attachments area (see [Cell Contents](#cell-contents) above). An attachment is **immutable**: once added, its content is never updated in place by any role, so a correction means deleting it and adding the corrected file. Vladimir and Sergey call this an *immutable document*, a PDF being their example.

A file the member adds to the cell without attaching it is instead their own **private** file, which no other member ever receives. Every row below reads the same for one, with a single difference: both *another member's* rows become `n/a`, since no other member ever has one of this member's private files to read or delete. A service reaches exactly what its principal reaches — its access is its principal's access (see [Cell Interface](#cell-interface) below) — so a member's own agent or backup service sees their private files, and a service acting for another member never does.

| Capability | Owner | Member | Service | 
|---|---|---|---|
| Read own attachment | yes | yes | yes | 
| Read another member's attachment | yes | yes | yes | 
| Add own attachment | yes | yes | yes | 
| Add an attachment as if authored by another member | no | no | no | 
| Update own attachment | no | no | no | 
| Update another member's attachment | no | no | no | 
| Delete own attachment | yes | yes | yes | 
| Delete another member's attachment | yes | no | no | 

- **Read own attachment** / **Read another member's attachment** — retrieve an attachment's content, one's own or one added by a different member.
- **Add own attachment** — put a new file into the cell's flat attachment set, authored as oneself.
- **Add an attachment as if authored by another member** — attribute a newly-added attachment to a member other than oneself. No role may do this.
- **Update own attachment** / **Update another member's attachment** — modify an existing attachment's content in place. No role may do either: an attachment is immutable, so replacing one means deleting it and adding the corrected file, which re-dates it and re-attributes it to whoever added the replacement.
- **Delete own attachment** — remove an attachment one added oneself.
- **Delete another member's attachment** — remove an attachment a different member added.

Two further capabilities move a file across the boundary between the two sets. Attaching one's own private file is just *Add own attachment* above; the reverse direction is its own capability:

| Capability | Owner | Member | Service | 
|---|---|---|---|
| Make own attachment private | yes | yes | yes | 
| Make another member's attachment private | no | no | no | 

- **Make own attachment private** — move an attachment one added oneself back among one's own private files. Every other member sees this as a deletion, which every role may already do to an attachment of their own.
- **Make another member's attachment private** — do the same to an attachment a different member added. No role may, owner included. The objection isn't the deletion — an owner may delete another member's attachment outright — but keeping a copy of a file every other member has been told is gone.

#### Note Permissions

A cell has **exactly one note** (see [Cell Contents](#cell-contents) above and [Note Area](#note-area) below) — never more. Vladimir and Sergey call this a *mergeable document*, and their own row labels distinguish a member's "own" document from "another member's"; with one note per cell that split does not arise, so the rows below are stated as capabilities on the cell's single note. Every member may write to it, regardless of ownership — reading and writing the note is the one surface where the owner/regular-member distinction does not apply at all. There is no commenting or suggested-edit mechanism of any kind — no margin comments, no proposed inline changes, and so no accept-or-reject step; a member simply edits the note, and every other member sees the result.

| Capability | Owner | Member | Service | 
|---|---|---|---|
| Read the note | yes | yes | yes | 
| Create the note | yes | yes | yes | 
| Create the note as if authored by another member | no | no | no | 
| Edit the note | yes | yes | yes | 
| Delete the note | yes | yes | yes | 

- **Read the note** — retrieve the note's current text.
- **Create the note** — bring the cell's note into existence, where it does not exist yet.
- **Create the note as if authored by another member** — attribute a newly-created note to a member other than oneself. No role may do this.
- **Edit the note** — commit a change to the note's text, with no review step. Since a cell has one note that every member may write, there is no distinction between editing one's own text and editing another member's; Vladimir and Sergey's own two edit rows collapse into this one for the same reason.
- **Delete the note** — remove the cell's note. Available to every member, since a member who may edit the note may in any case blank it.

#### Tool & Member Info Permissions

These govern the graph claims backing a cell's `c:member` and tool content — what Vladimir and Sergey call a *claim*. Every row is scoped by claimant: a member's own claims are the ones they themselves claim. **A claim is editable, as the user experiences it.** A member who wants to correct their email address in a `c:member` graph just edits the field, and the app presents that as an ordinary update — which is why the `Update own claim` row below reads `yes`.

Underneath, at the **PDN layer**, there is no update operation on a claim at all: a claim is immutable, and the app implements the edit by deleting the claim carrying the old email address and issuing a fresh claim carrying the new one. Nothing about that reaches the user — they see a field they changed, not a retraction and a re-issue. The graph itself is never replaced either way; it stays one evolving graph whose claims come and go beneath it.

This document describes the first of those two layers, so every row below is the user-level rule. Vladimir and Sergey's own tables describe the second, which is why their `Update own claim` row reads `no` where this one reads `yes` — the two are not in conflict, they are the same behavior seen from either side of that boundary.

| Capability | Owner | Member | Service | 
|---|---|---|---|
| Read own claim | yes | yes | yes |  
| Read another member's claim | yes | yes | yes |  
| Issue own claim | yes | yes | yes |  
| Issue a claim as if issued by another member | no | no | no | 
| Update own claim ¹| yes | yes | yes |  
| Update another member's claim | no | no | no | 
| Delete own claim | yes | yes | yes | 
| Delete another member's claim | yes | no | no | 

¹ User-level, this is an ordinary edit of one's own claim. At the PDN layer the claim is immutable and the edit is carried out as a delete plus a fresh claim — which is what Vladimir and Sergey's `no` records. Same behavior, different layer.

- **Read own claim** / **Read another member's claim** — read a graph claim, one's own or one another member claims. Read access is unrestricted across the cell.
- **Issue own claim** — assert a new claim as claimant, in a `c:member` graph or a tool's own graph one claims oneself.
- **Issue a claim as if issued by another member** — attribute a newly-issued claim to a claimant other than oneself. No role may do this.
- **Update own claim** — change the value a claim one issued oneself carries, e.g. correcting one's own email address. An ordinary edit as far as the user is concerned; a delete-and-re-issue underneath (see above).
- **Update another member's claim** — change a claim a different member issued. No role may do this at either layer: write access is always scoped to one's own claimant identity.
- **Delete own claim** — retract a claim one issued oneself.
- **Delete another member's claim** — retract a claim a different member issued.

### Naming, Renaming, and Sharing

For a single-member cell or a cell with three or more members — or a two-member cell that also carries a tool — any member of the cell — not just its creator or another owner — can rename it, and the new name propagates to every member: renaming is never gated by ownership, unlike other-member claim/attachment deletion (see [Permissions](#permissions) above). Chat likewise stays freely editable by every member regardless of ownership status, and any member may add or delete their own attachments — though no member may update an attachment in place, since an attachment is immutable, and what a member keeps among their own private files rather than attaching is their own affair, gated by nothing. This mirrors how **Slack** and **Notion** handle renaming by default: any member/editor can rename a channel or page, and the new name propagates to everyone. It's a deliberate contrast with **Microsoft Teams** (channel owners only, by default), **Discord**, and **GitHub**, which restrict renaming to a privileged admin/Manage-Channels/owner role — a distinction the app's cell model doesn't have to begin with. A bare two-member cell — one carrying no tool — does *not* follow this rule — see the exception below.

A cell's name must be unique among its sibling cells — the cells directly nested under the same parent. When a user renames a cell — e.g. to give it a name of its own choosing, different from its category's label, the same convention followed by other PKM tools — to a name that already belongs to one of its siblings, the app doesn't prompt or reject the input: it silently appends the next available integer suffix (`"1"`, `"2"`, ...) to make the name unique. The same rule applies when creating a brand-new cell whose default name (e.g. copied verbatim from its category's own label) would otherwise collide with an existing sibling. In this repo's scaffolding one name is reserved outright rather than suffixed: no cell may be named `_cell-attachments`, that being the one subfolder of a cell's folder the app owns (see [Scaffolding: This Repo's Filesystem Tree](#scaffolding-this-repos-filesystem-tree) above).

This same uniqueness rule applies on **receipt** of a shared cell — for two-member cells and cells with three or more members alike — and, once a bare two-member cell's name goes independent per member (see the exception below), on every later rename by either member too: if the incoming or renamed name collides with a cell the recipient already has at that position in their own tree, the app appends the next available suffix to it rather than overwriting the existing cell or rejecting the incoming/renamed one.

**Exception: bare two-member cells (carrying no tool).** A two-member cell's name is never shared, synced content between its two members, in contradiction to the general rule above — each member is independently responsible for the name on their own side — but *only* when that cell carries no tool. This is because a bare two-member cell is an asymmetric dyad about the relationship *between* its own two members: each member's name for it naturally reflects their own perspective on the *other* party, and there's no single name that fits both (e.g. Alice's cell with Bob, below). A two-member cell that does carry a tool, by contrast, is about a third party neither member's own perspective differs on — its derived subject (see README.md's [Cell Ontology](README.md#cell-ontology) section) is the same graph-linked subject regardless of which member is looking, so there's no asymmetry to preserve, and it follows the general shared-name rule above instead, exactly like a cell with three or more members (a genuine group identity with no single "other side" to name from either). For example, the `Medical Appointment` cell Alice shares with her husband Dave — a two-member cell whose one form tool is about their daughter Sophia — has one shared name kept in sync on both sides, renamable by either Alice or Dave. Their `Sophia Walker` cell (see example.md's [Taking Care of Sophia](example.md#taking-care-of-sophia)) has the same shape and follows the same rule.

For a bare two-member cell, the creator's name for their own copy is simply whatever they set it to — chosen and renamed exactly as for any other cell, subject only to the sibling-uniqueness rule above, but never propagated to the recipient's copy.

At **first-time receipt** of a bare two-member cell — the recipient self-evidently did not create it, they're joining one already created — the app does not just adopt the creator's name as shared content. Instead, once, at that first receipt, it analyzes the `c:member` graph(s) belonging to the cell's creator/sender member and auto-generates a name for the cell from that analysis. (The sender's own choice of name for their copy is naturally centered on their own perspective, so blindly reusing it verbatim on the recipient's side would be a poor fit; analyzing the sender's own member graphs lets the recipient's app derive a name that makes sense from its own side instead.) This auto-generated name is subject to the same sibling-uniqueness suffixing described above.

For example, Alice creates a bare two-member cell about her relationship with Bob and names it "Bob" on her own side, then shares it with Bob. On first receipt, Bob's app doesn't just copy "Bob" — that's Alice's name for *him*, not a name that makes sense in Bob's own tree. Instead it scans the cell's `c:member` graph(s) belonging to Alice, finds a graph about Alice herself, extracts her given name, and names the cell "Alice" on Bob's side instead.

From that point on, both the creator's and the recipient's names for their own copies may be freely renamed at any time, exactly like a single-member cell's name — but such a rename stays purely local to the renaming member's own tree and is never propagated to the other member's copy, in either direction. This is what keeps the first-receipt divergence meaningful: if a later rename on either side rippled to the other, it would silently overwrite a name chosen to fit that member's own perspective, defeating the reason the divergence exists in the first place.

### Wikilink-Triggered Cell Creation

A cell's note may contain a wikilink with no target id at all yet — one whose linked-to name has never been instantiated as a cell by anyone (see [Cell Contents](#cell-contents) above for how an already-instantiated link instead resolves by stable id, not display text). Since a note is never a standalone unit in this app — it's always the single note *of* a cell, never anything on its own — clicking such a truly-new link can't create an orphan note the way a flat-file PKM tool would; the only creatable target that actually fits the model is a new cell.

Clicking a no-id wikilink therefore creates a new cell named after the link text (e.g. `[[foo]]` creates a cell named "foo"), placed as a direct child of the top-level tree root — the same "new note at the root, move it later" behavior familiar from PKM tools, but scoped to a cell rather than a bare note. The user is expected to move the new cell to a more appropriate position afterward, exactly like any other cell; the sibling-uniqueness auto-suffix rule described in [Naming, Renaming, and Sharing](#naming-renaming-and-sharing) above applies here too, if "foo" collides with an existing top-level cell. Creating the cell also derives its stable, globally-unique id — from the creator's PDN ID, a public key of the creator's identity and fresh random bytes (see [Cell Id](cell-databook.md#cell-id)), not the small sequential `cell-<NN>` this repo's own example data uses — and rewrites the clicked link, in the clicking member's own copy of the note, from `[[foo]]` to `[[7f3a9c2e5d41b08f…|foo]]` (id before the pipe, unchanged display text after), so every later click by anyone who has access to that same cell resolves deterministically to it — never by re-matching on the display text "foo."

The new cell carries no `c:category` at all — the user didn't pick any existing category concept, so this is the same **Custom** case described in [Cell Contents](#cell-contents) above (carrying no category value at all; `foo(custom).databook.md` in this repo's scaffolding). It is a single-member cell, created by and with `:Self` as its sole member, following the same minimal-stub-graph pattern used elsewhere for a cell with nothing substantive to say yet (e.g. the bare given-name claim in Sophia Walker's Health & Wellness cell or her primary care physician's cell — see example.md). Its own note starts out blank, ready for the user to fill in.

This creation behavior is strictly for the no-id case. A wikilink that already carries a target id — one pointing to a real, already-instantiated cell the sender has, but that the clicking member doesn't have in their own tree (e.g. it was never shared with them, or they organize their tree completely differently) — must never fall back to creating a same-named stub cell either: doing so would produce an empty, disconnected cell that visually masquerades as the real target, reintroducing a milder version of the same misdirection risk id-based resolution exists to prevent. That case instead renders as unresolved/inaccessible, exactly as described in Filesystem Persistence above — creation is reserved for links whose target has literally never existed anywhere.

### Auto-Filing on Receipt
 
When a cell is shared with someone who doesn't yet have the app, receiving it — e.g. clicking an invite link — triggers installation, and the app must then decide where to file the incoming cell in the recipient's own tree of cells.

For example (see example.md's ["Caring for Ginger"](example.md#caring-for-ginger) for the underlying cell and graphs): imagine Paula doesn't use the app yet, and the invite link from Alice to [cell 40](<example/Cells/Pets/Ginger/Medical/Medical.databook.md>) causes Paula to click on the link and download/install it. The app receives the cell, but where should it file it on Paula's side? Paula's app examines the cell, looks at its category type "Medical," and makes a good (though not perfect) guess to create the following tree of empty cells: People > Others > Alice > Pets > Ginger, and files the incoming cell as a new child of that Ginger cell.

Ideally it would have filed the cell shared by Alice's app under People > Immediate Family, because she is Paula's daughter, but Paula's app didn't know that, so it did the best it could. To perfect things, Paula can create an Immediate Family cell under her People cell and move Alice (and sub-cells) under it.

### Organize

There are two kinds of organizing that the app does when the user selects a cell and taps " Organize":

* **Auto File**: It examines the selected cell and if it doesn't have a category, suggests one and then automatically files it there if the users wishes.
* **Divide and Conquer**: It looks inside the cell (especially the cell's note) and does the following.

#### Auto File

The app might look at the chat and/or Note and say "Hmmm...this looks like it's about taking care of your cat. Would you like me to file it under Cells > Pets? 

#### Divide and Conquer

The app looks at the Note, and moves chunks of content out it, leaving behind a link where the chunk was. It then creates a new categorized cell from this chunk of content. The category would come from an examination of the contents. 

Here's an example. Imagine a cell that contained lots of notes about Alice's mother Paula. In that stream of notes was Paula's credit card info (name, number, expiration date, CVV, etc.). The app removes this chunk of content leaving behind a link called "Paula's Credit Card". If Alice taps this link it brings her to a new cell called "Paula's Credit Card" of type `cat:BankingPayments` with a Form tool that contains the credit card info, but parsed into fields and values. It automatically files this new cell under Cells > Immediate Family > Paula Walker > Finances > Banking & Payments.

It could then ask some questions, do you know the name of the bank that issued this card? (to which Alice answers "GiantBank"). Would you like me to rename this new cell "GiantBank - Mastercard"? etc. 


### Finding Cells by Tag

The two kinds of tag a cell can carry, and what each is for, are described in [Tags](README.md#tags) in README.md. The user can search their tree for a tag: the result is a flat list of links to cells — not a filtered tree, and not the cells' contents — from which tapping an entry opens that cell. Searching **Ginger** returns links to all three of her cat's cells at once.

Each result links by the target cell's own stable id, exactly as a resolved wikilink in a note does (see [Cell Contents](#cell-contents) above). This matters for the same reason it matters there: cell names are only unique among siblings, never globally, so resolving a result by name could land on an unrelated cell that happens to share a display name with the intended one. Id-based resolution rules that out.

What this search matches is **user-defined tags only**. A hidden service tag is hidden from the user's retrieval exactly as completely as it is hidden from their display: the user cannot find a cell by one, cannot see one in a result, and has no query — free text or otherwise — that turns one up. Searching *Christmas List* finds nothing on the strength of the Apple Contacts tag alone. What a service can do with its own tags is a separate, non-user-facing matter; see [Service Tag Access](#service-tag-access) below.

Results are scoped to the searching member's own tree.


### Finding Cells by Property

Tags are not the only way to gather cells. The user — or their own AI agent, working on their behalf — can also search for every cell whose tool graph carries a given **property**, and get back the same flat list of cell links a tag search returns.

The worked example is the one a tag would otherwise have handled: "show me every cell where I hold a loyalty program." That is a search for `sa:loyaltyProgramID` (see [Service Accounts Ontology](README.md#service-accounts-ontology) in README.md), and it returns Alice's `Hilton` cell because that cell's tool graph records her Hilton Honors membership number. Nobody had to label the cell for this to work.

The two searches complement each other rather than competing. A property search needs no one to have remembered to tag anything and cannot drift out of date, since it reads the same fact the cell already stores for its own sake — but it only reaches what the data actually models. A tag reaches anything at all, including a grouping that exists only in the user's head ("Ginger"), at the cost of someone having to apply it. So a fact with a property of its own is found by that property, and a tag is for what the data does not already model — which is why the app ships no built-in tag vocabulary.

### Adding a Tool

Every cell offers an **Add Tool** action, whether or not it already carries one — a cell cloned from a template that declares no tool starts with none (see [Lazy Instantiation](#lazy-instantiation) above). The user selects the cell, taps **Add Tool**, and a modal dialog asks them which tool to add and, for a **Form**, which template the new form's information should follow. The default selection is **Contact Info** (`pshapes:ContactInfoShape`) — the same contact-info shape every cell's `c:member` graph already uses — since a form about a person who is not themselves a member of the cell is the commonest case by far. The dialog offers many other choices alongside it, one per SHACL shape a tool's graph can be validated against — **Passport**, **Debit Card**, **Vehicle**, **Trip Itinerary**, and the rest; [Form Types](#form-types) below lists all of them.

Whichever template the user picks is stamped directly onto the new graph as its `c:shape` value — the same value Lazy Instantiation would have stamped automatically had the category's own template declared the tool up front — and the form the app renders for filling it in is derived from that same shape (see [Form Fields from SHACL Shapes](#form-fields-from-shacl-shapes) below). The user also names what the tool is about, which becomes its single `c:formTopic`.

**Any cell can gain a tool this way, as many as the user likes.** The action is not restricted to categories whose template declares one, and the picked template does not have to be one the cell's own category declares: the dialog offers the full list of shapes regardless, and whatever the user picks is stamped onto the new graph as-is. A category's `c:TemplateCell` therefore has no authority over a hand-added tool, and a category that declares no tool offers no shape hint either — integrity.md's TTL-4 deliberately does not check such a tool's graphs against the category at all.

Nothing caps how many tools a cell may hold. What the cell's own member count does cap is the number of graphs beneath any one tool — one per claiming member (YAML-8) — which applies equally to a tool the template declared and one the user added. Alice's Immediate Family cell for her daughter Sophia (cell-12) is the worked example of the manual path: `cat:ImmediateFamily` declares no tool, and Sophia has no instance of the app and so cannot be one of the cell's members, so Alice adds a Form tool about her by hand, picking Contact Info herself.

#### Form Types

A form type *is* a SHACL node shape: picking one in the **Add Tool** dialog stamps that shape's IRI onto the new graph as its `c:shape` value, and the fields the app renders are derived from it (see [Form Fields from SHACL Shapes](#form-fields-from-shacl-shapes) below). The table is the complete list the app ships — the same shapes a `c:TemplateCell` draws on for its `c:formShape`, offered to the user directly. Each is defined in the `*-shacl.ttl` file paired with the ontology that declares the class it targets; see [core-files.md](core-files.md) for those files.

The last column names the categories whose template declares that shape up front, so a cell of that category is created carrying the form already (see [Lazy Instantiation](#lazy-instantiation) above). A dash means no template declares it — the shape is reachable only by adding the tool by hand, which is exactly what the dialog is for. Either way the full list is offered regardless of the cell's own category.

<!-- BEGIN GENERATED: form-types (helpers/form-types.py) -->
| Form type | `c:shape` value | What the form records | Declared by |
|---|---|---|---|
| **Contact Info** | `pshapes:ContactInfoShape` | A person's names, organization name and unit, job title, emails and phones, postal addresses, online services, anniversaries, personal info and photo. Given name required, at most one of each component. The dialog's default, and the same shape every template names as its `c:memberShape` | `cat:PrimaryCarePhysician` |
| **Health & Wellness** | `pshapes:HealthWellnessShape` | A person's physical characteristics — height, eye color, hair color; all optional | `cat:HealthWellness` |
| **Primary Care Physician** | `pshapes:PrimaryCarePhysicianShape` | A physician's medical specialty; optional, and paired with Contact Info on the same form | `cat:PrimaryCarePhysician` |
| **Directory Profile** | `dpshapes:DirectoryProfileShape` | What a membership directory asks of a member — member since, sponsor, industry, previous positions, directorships, non-profit positions, recognitions, spouse or partner, family, hometown, dietary restrictions, personal goals, life experiences; nothing required | — |
| **Education Record** | `educationshapes:EducationRecordShape` | One stage of a person's schooling — school name (required), education level, school city and state, year graduated, degree | — |
| **Social Security Number** | `pshapes:SSNShape` | A US Social Security Number, in `NNN-NN-NNNN` form | `cat:SSN` |
| **Passport** | `idocshapes:PassportShape` | Name, date of birth, passport number and expiration date (all required); additional name, issue date, issuing country, place of birth, gender marker and photo | `cat:Passport` |
| **Driver's License** | `idocshapes:DriversLicenseShape` | Name, date of birth, license number and expiration date (all required); additional name, postal address, issuing jurisdiction and photo | `cat:DriversLicense` |
| **Birth Certificate** | `idocshapes:BirthCertificateShape` | A full name, or a given plus family name; additional name, alternate name, nickname and legal name are optional | `cat:BirthCertificate` |
| **Service Account** | `sashapes:ServiceAccountShape` | An online account — username and password (required); service name, service URI and loyalty program ID | `cat:BankingPayments`, `cat:Companies`, `cat:TravelProvider` |
| **Debit Card** | `bankingshapes:DebitCardShape` | Card number and expiration date (required); CVV, and a link to the checking account it draws on | `cat:BankingPayments` |
| **Checking Account** | `bankingshapes:CheckingAccountShape` | Exactly one account number and one routing number | `cat:BankingPayments` |
| **Residence** | `residenceshapes:ResidenceShape` | A place lived in — exactly one address and one temporal interval (an open-ended one meaning current), plus the resident | `cat:Home` |
| **Vehicle** | `vehicleshapes:VehicleShape` | Vehicle type, make, model and model year (all required); VIN, color, body type, fuel type, drive wheel configuration, odometer reading and engine specification | `cat:Vehicles` |
| **Pet** | `petshapes:PetShape` | A pet's name and species (required); breed, birth date, body weight, sex and spay/neuter status | `cat:Pets` |
| **Pet Care & Feeding** | `petshapes:PetsCareAndFeedingShape` | The same fields as Pet, every one optional, so day-to-day care instructions may identify the pet by any subset of them or none | `cat:PetsCareAndFeeding` |
| **Pet Medications** | `petshapes:PetMedicationRecordShape` | At least one medication, each with its active ingredients, dosage amount and administration schedule | `cat:PetsMedical` |
| **Medical Appointment** | `mashapes:MedicalAppointmentRecordShape` | Patient, insurance provider and policy number (required); primary care physician, insurance group number, preferred pharmacy and medical history notes | `cat:MedicalAppointment` |
| **Trip Itinerary** | `itineraryshapes:ItineraryShape` | A trip's plan as free text — at least a human-readable label or description, the itinerary being drafted and revised in prose rather than in fixed fields | `cat:Trips` |
| **Organization** | `oshapes:OrganizationShape` | An organization's own profile — website and member or employee count, alongside its name and self-description | `bhscat:BostonHubSociety`, `cat:Groups`, `cat:Organization` |
<!-- END GENERATED: form-types -->

An installed [category extension](README.md#category-extensions) can reach this list from either side. Its template may declare a shape already here — `bhscat:BostonHubSociety` declares `oshapes:OrganizationShape`, which is why that row's last column names a concept outside `cat:CategoryScheme` — or it may publish a shape of its own, which then joins the dialog alongside these. What an extension publishes as its template's `c:memberShape` is a different matter: `bhsshapes:MemberShape` governs that category's member graphs rather than a form, so it is not a form type and is not offered here.

The other three tool kinds — `c:Calendar`, `c:Canvas`, `c:Map` — have no content model yet, so they have no type list of their own: the dialog asks which template to follow only for a **Form**.

The table above is generated from the `.ttl` files by `helpers/form-types.py` — the shapes and the last column come from `helpers/validate.py`'s own shape registry and from every `c:formShape` in `cat-templates.ttl` and `category-ext/`, so a new shape or a newly-declaring template shows up as drift rather than being missed. The names and descriptions are written by hand. Run `python3 helpers/form-types.py --check`, or `/sync-form-types`, to reconcile the two.

### Note Area

The Note area is a Markdown editor for the cell's one note, providing the functionality typical of Markdown editors:

- Freeform Markdown syntax editing — headers, bold/italic/strikethrough, inline code and fenced code blocks, blockquotes
- Bulleted, numbered, and nested lists, plus checklist/to-do items
- Tables
- Links — ordinary URLs and `[[wikilinks]]` to other cells' notes, with autocomplete as the user types (see [Cell Contents](#cell-contents) above for how a wikilink actually resolves to a target cell's id)
- Inline image/embed preview
- Live preview of rendered Markdown, kept in sync with the raw source
- Find and replace
- Undo/redo
- Continuous autosave — there is no explicit save step
- Editable by every member regardless of ownership (see [Permissions](#permissions) above). There is no commenting or suggested-edit mechanism, so nothing is stored in the note beyond its own Markdown, keeping it portable

### Chat Area

Chat is one feature with two visibility modes, not two separate concepts. By default, every message posts to the cell's one shared group stream, visible to every member. Any message can additionally be *directed* at a specific named member — human or agent — while staying in the shared stream (e.g. Alice @-mentions her agent; every member sees both her prompt and the agent's reply). Separately, a true private 1:1 thread between a member and their own agent is also supported, whose transcript is not visible to other members — only the *resulting* committed changes (note edits, tool-graph revisions, new attachments) surface into the shared cell.

### Inviting services

A member may invite a service — their own AI agent, a backup service, or an organization's own service provider — into a cell, where it becomes a real member alongside the human ones. What the user is doing in each case, and what access the invitation grants, is below; what an invited service can then actually do inside the cell, and how the app runs it on the member's device, belongs to the module rather than the UI and is covered under [Services](#services).

#### Inviting AI Agents

A member may invite their own AI agent (`s:ChatGPT`, a leaf under `s:AgentService` — see README.md's [Service Ontology](README.md#service-ontology)) into a shared cell — e.g. inviting ChatGPT to help plan a trip in a `cat:Trips` cell. An invited agent becomes a real cell member: it gets its own self-claimed `c:member` entry alongside the human members, which raises the cell's own distinct-member count (e.g. Alice + her own agent = two distinct members, a two-member cell; a third member joining too — human or service — would raise it to three members, the same derivation applying regardless of count — see [Number of Members](#number-of-members) above). Because the agent is a literal member, it needs no special-case permission logic — [Permissions](#permissions) above already covers it: by default, an invited agent gets exactly the same read/write access to the cell's note, files, and [chat](#chat-area) that any non-owner human member has (see [Permissions](#permissions) above) — and, unlike a human member, a service member can never be promoted to owner, so it stays at that baseline permanently.

#### Inviting Backup Services

{to be written}

#### Inviting Service Providers

{to be written. Inviting Cititbank, etc.}

## UI Implementation
### Form Fields from SHACL Shapes

When the app renders an editable form for a cell's `c:member` content or for a `c:Form`'s own content, it derives each input field directly from the applicable SHACL shape — found live by matching the cell's own `c:category` value against `cat-templates.ttl`'s `c:TemplateCell` individuals and reading either that template's `c:memberShape` (for a `c:member`-content form) or the `c:formShape` of the tool it declares (for a tool's own form) (see [Lazy Instantiation](#lazy-instantiation)), rather than hand-coding one form per template class. A tool the user added by hand takes its shape from the user's own pick instead (see [Adding a Tool](#adding-a-tool) above). Each `sh:property` constraint on that shape becomes one form field: `sh:datatype`/`sh:class`/`sh:nodeKind` determines the field's input type, and `sh:minCount`/`sh:maxCount` determine whether it's required and whether it repeats.

A property whose `sh:property` constraint carries an `sh:in` list renders as a closed dropdown populated directly from that list, with no further query needed — the shape itself is authoritative for what's selectable. This covers both a literal-value enumeration (e.g. `v:fuelType`, `v:driveWheelConfiguration`) and a class-value-punned one (e.g. `v:hasVehicleType`, whose `sh:in` list is the four concrete classes `v:Car`/`v:BusOrCoach`/`v:Motorcycle`/`v:MotorizedBicycle` rather than a set of literals).

A property constrained only by `sh:nodeKind sh:IRI`, with no `sh:in` list — e.g. `v:hasMake`, `v:hasModel` — tells the app the field's *shape* but not its *legal values*. For a field like this, the app instead queries the ontology graph for every individual typed the property's expected range class, and uses each one's `rdfs:label` as the dropdown's display text and its IRI as the stored value: every `v:Make` individual for `v:hasMake`, every `v:Model` individual for `v:hasModel`. This is a general pattern, not special-cased to vehicles — it applies to any `sh:nodeKind sh:IRI`-only property with an open, ontology-defined vocabulary rather than a small fixed one.

Where one such field's legal values depend on another field already filled in, the app narrows the query accordingly rather than presenting two independent pickers. `v:hasModel`'s dropdown is filtered to only the `v:Model` individuals whose `v:modelMake` points back at the already-selected `v:hasMake` value — a cascading, make-then-model picker. Alice's RAV4 cell illustrates this: choosing "Toyota" narrows the model dropdown to Toyota's own vendored models before "Toyota RAV4" can be selected (see example.md's ["Vehicles"](example.md#vehicles) for the underlying cell and [graph 63](<example/Cells/Things/Vehicles/RAV4/RAV4(vehicles).databook.md#graph-63>)).


## Services

Every service the app offers *is* one of the classes in README.md's [Service Ontology](README.md#service-ontology) — there is no separate wrapper concept sitting over one. What the app ships per service is the code that runs it on the member's own device, translating between the external system's own API and the cell, which it reaches through the [Cell Interface](#cell-interface) like any other member, with that member's own access and no more.

Each principal runs their own services independently — their own credentials, their own connection to the underlying external system — the same way each peer already manages their own tree position for a shared cell independently (see [Cell Storage](#cell-storage) above). An AI agent runs whenever a message addressed to it arrives (matched via `s:actsFor`); a contact sync or a backup service runs on its own schedule instead. Because a service acts for exactly one member, everything it records privately stays on that member's side — which is the whole reason a hidden [service tag](README.md#tags) never propagates on a share.

Three are documented below. All three are `s:AgentService`s, meaning each acts for exactly one member:

| Service | Class | What it does |
|---|---|---|
| ChatGPT | `s:ChatGPT` | An LLM assistant that collaborates in the cell's chat, note, and tool graphs |
| Apple Contacts | `s:AppleContacts` | Syncs a member's address book into and out of cells |
| Arca Backup | `s:ArcaBackup` | Backs up the member's own copy of a cell |

An `s:ServiceProvider` — an organization's own service, such as Citibank's — is equally a service by this definition; it simply acts for the organization that provides it rather than for a member, and the app does not ship its code.

### Cell Interface

Every `s:Service` reaches a cell through one and the same surface, the **Cell Interface**: the read and write operations over a cell's [note](#note-area), [attachments](#cell-contents), [chat](#chat-area), and `c:member`/tool claims. There is no side door — no service reaches a cell's content by any other route, or writes to another member's claims directly, and none gets an API of its own.

This is why an invited service needs no special-case permission logic anywhere in this document. The Cell Interface is the same surface a human member's own UI uses, and it enforces the same rules for both, already set out in [Permissions](#permissions) above:

- **Read access is unrestricted across the cell** — every member, human or service, can read the note, every member's and every tool's claims, and attachment metadata. "Across the cell" means the cell's shared content: a member's own private files are not part of it, and a service reaches them only when it acts for that member, its access being its principal's access.
- **Write access is scoped to the caller's own claimant identity** — a service creates, updates and deletes only the claims it claims itself. It can edit the shared note and add attachments like any member, but it can never write to another party's `c:member` graph or tool graph.
- **A service is never an owner.** It cannot be promoted (`c:owner`'s range is `p:Person`), so it permanently sits at the non-owner baseline: it cannot delete another member's claims or attachments, and it cannot delete the cell for everyone.
- **Its access is its principal's access.** An `s:AgentService` operates with the access of the one member it `s:actsFor`, never more — inviting an agent grants it nothing its principal did not already have.
- **Hidden [service tags](README.md#tags) are namespace-scoped.** A module searches, reads, adds and deletes only the `c:serviceTag` nodes carrying its own developer's `c:tagNamespace`; another module's are neither readable nor writable, and none of them is exposed to the user's own UI at all.

What a service does *beyond* the cell — call an LLM, read an address book, write a backup — is its own business and is not the Cell Interface's concern. The interface's job is that everything arriving back *in* the cell arrives through the same door, under the same rules, as a person's own edits.

### Service Tag Access

A module reaches the [hidden service tags](README.md#tags) it has written through the [Cell Interface](#cell-interface), like everything else it touches in a cell. This is not the user's tag search under another name: the user's search never matches these tags at all (see [Finding Cells by Tag](#finding-cells-by-tag) above), and a module does not search them by free text but by `c:tagNamespace` and `c:tagKey` — which is what those two parts are for.

The interface scopes **every** service-tag operation — search, read, add, delete alike — to the namespace the calling module's developer controls. The Apple Contacts module therefore searches, reads, adds and removes `foundation.mee.applecontacts` tags and nothing else: another module's tags are not merely absent from its results, they are unreadable and unwritable. That isolation between services is the namespace's whole job; it is not a display convention layered over one shared pool.

Two practical consequences for a module. First, results are scoped to its own member's tree, so a tag is only ever reachable in the instance that wrote it — consistent with its never being shared. Second, two identical tags are two separate tags, not one: nothing deduplicates them, so a module adding a tag checks whether the cell already carries that exact namespace/key/value combination before writing another.

### The Iterative Prompt/Response Loop

Each turn of a member's conversation with the agent proceeds as follows:

1. The member sends a message — in the shared group stream (optionally @-directed at their agent) or in a private DM thread with their agent.
2. Their own device — running their agent service, invoked on receiving a message addressed to it (matched via `s:actsFor`) — assembles context: the shared note's current text, the agent's single evolving tool graph (its accumulated understanding of the trip, or whatever the cell concerns), recent relevant chat turns, and existing attachment metadata (filenames/captions).
3. This context plus the new message is sent to the underlying LLM service (push model — the app calls out; no inbound endpoint is ever exposed).
4. The response is applied as one atomic turn, all under the agent's own existing member-level write rights:
   - a conversational reply posted back into the same stream/thread the prompt came from (group-visible or private, matching where it arrived);
   - the agent's tool graph revised in place to fold in this turn's new facts/decisions — a single evolving graph, not a new one per turn, mirroring how the note itself is one living document rather than a new file per edit;
   - optionally, a direct edit to the shared note, and/or a new attachment (e.g. a fetched photo of a hotel or landscape) added to the cell's flat set of attachments.

Nothing currently records *which* conversation (group vs. private) produced a given note edit or tool-graph revision — an accepted limitation, not a defect, worth knowing if audit-level provenance ever matters.

### ChatGPT Service

This module lets a member invite OpenAI's ChatGPT into a cell as a real `s:ChatGPT` member (see [Inviting AI Agents](#inviting-ai-agents) and README.md's [Service Ontology](README.md#service-ontology)). At a high level, once invited, it does four things:

1. **Participates in the cell's chat.** It posts and receives messages through the same group/directed/private-DM model described in [Chat Area](#chat-area) above — no separate messaging channel of its own.
2. **Reads all of the cell's data.** Unlike its write access (below), read access is unrestricted: the note's current text, every member's `c:MemberGraph` and every tool's `c:FormGraph` content, and attachment metadata are all available to it as context for each turn — this is the raw material the [Iterative Prompt/Response Loop](#the-iterative-promptresponse-loop) assembles on its behalf.
3. **Writes edits to the note.** Because it's a real cell member, it has the same free note-editing rights [Permissions](#permissions) already grants any member — no agent-specific carve-out is needed.
4. **Creates, reads, updates, and deletes its own claims, as claimant** — but only within the two graphs it actually claims:
    - **Its own `c:member` entry** — the self-claimed graph proving its membership (e.g. [graph 67](<example/Cells/Travel/Trips/Kyoto Trip 2027/Kyoto Trip 2027(trips).databook.md#graph-67>)'s `s:actsFor` claim) — content *about itself*.
    - **Its own tool graph (or graphs)** — content about whatever the cell's relationship concerns (e.g. [graph 70](<example/Cells/Travel/Trips/Kyoto Trip 2027/Kyoto Trip 2027(trips).databook.md#graph-70>)'s evolving itinerary) — content about *the tool's topic*, distinct from any other member's or party's own claims about that same topic.

   It never writes to a graph claimed by someone else — not another member's `c:member` entry, not a tool graph another party claims — read access is unrestricted, but write access is always scoped to the module's own claimant identity. In the steady state this means revising its tool graph in place turn by turn (see [The Iterative Prompt/Response Loop](#the-iterative-promptresponse-loop)); "create" and "delete" cover the initial contribution and retracting a claim that's no longer accurate (e.g. a cancelled leg of an itinerary), respectively. Each of those revisions is a delete-and-re-issue at the PDN layer, exactly as for a human member's own edit (see [Tool & Member Info Permissions](#tool--member-info-permissions) above).

### Apple Contacts Service

This module lets a member sync their Apple Contacts address book into and out of cells, as an `s:AppleContacts` member. It has no LLM in it at all — what makes it an agent service is simply that it acts for exactly one member, syncing that member's own address book and answering to nobody else in the cell.

On **import**, each contact record becomes a graph, its vCard fields mapping onto the Persona ontology's own names, phone numbers, addresses, organization, job title, birthday, photo and so on. On **export**, the direction reverses: all of a person's graphs merge into a single vCard, each field value carrying the label of the graph it came from, since vCard's own model is one card per person with repeatable labelled fields.

The piece the cell model has nowhere else to put is an Apple Contacts **Group**. A group is not a category, not a topic, and not a member, so the module records it as a [hidden service tag](README.md#tags) on the cell — namespace `foundation.mee.applecontacts`, key `group`, value `Christmas List` for a contact that sat in a group of that name. Holding it on the cell is what makes the round trip **lossless** and the sync **bidirectional**: a later edit on either side can be carried back to the other, because the module can still tell which group the contact came from. Alice's `Bob Johnson` and `Fred Flintstone` cells both carry it.

That tag stays in the syncing member's own copy and is never shared, for the reason [Services](#services) gives: a service acts for one member, and a member whose instance runs a different service, or none, could neither interpret nor clear the value.
