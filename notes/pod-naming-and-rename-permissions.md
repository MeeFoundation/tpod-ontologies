# Pod Naming and Rename-Permission Model — Research Notes

## Overview

A pod's own name (its folder name / `title:` / databook filename root) is part of the pod's synced, shared content, not a purely local, per-member choice. That raises a natural question: since the name is shared and propagated to every member, *who* is allowed to trigger a rename? Other collaboration systems that share a single canonical name across members split roughly into two camps: **egalitarian** (any member can rename) and **privileged** (only a creator/owner/admin role can). This note captures the comparison used to decide which camp the app's pod model belongs in.

---

## Comparison

| System | Who can rename | Propagation | Collision handling |
|---|---|---|---|
| **Slack channel** | Any member, by default (workspace admins *can* restrict this to Owners/Admins, but it's open out of the box) | Single shared name — changes for everyone at once | Rejected outright if taken workspace-wide; user must pick another (no auto-suffix) |
| **Notion page/database** | Any editor | Shared, instant, for every viewer | No uniqueness constraint at all — sibling pages can share an identical title |
| **Microsoft Teams channel** | Team **owners only**, by default (a setting exists to allow members, but it's off by default) | Shared, single canonical name | Rejected if it collides within the team; no auto-suffix |
| **Discord channel** | Only members with the "Manage Channels" permission (mods/admins) | Shared | No uniqueness constraint at all — Discord allows duplicate channel names |
| **GitHub repository** | Admin-role holders only | Shared, canonical, with a temporary redirect from the old name | Rejected if taken in that namespace; no auto-suffix |
| **Trello board** | Any member with edit rights (i.e., not an "Observer") | Shared | No uniqueness constraint |
| **WhatsApp / Signal group** | Configurable — admins can restrict "edit group info" to admins only, but the default is *all participants* | Shared | None — duplicate group names can coexist in your own chat list |
| **Dropbox shared folder** | Any member, but **only for their own view** — Dropbox's own docs state a rename affects only you | **Not shared** — the opposite of the systems above | N/A — a rename is local, so no cross-member collision is even possible |
| **Google Drive shared folder** | Depends on the object: renaming the real folder (with edit access) is shared; renaming a "shortcut" / "Add to My Drive" copy is local-only | Both models coexist, on two different objects | Shared-object rename can collide; shortcut rename can't (it's local) |
| **Local-sync tools** (an Obsidian vault kept in sync, a cloned git repo) | Nobody "owns" the name — there's no canonical name to begin with; each copy's folder name is independently whatever its local user set | No shared identity at all | N/A |

## Observations

- The app's pod sits with the **single-shared-name** group (Slack, Notion, Trello, Teams, Discord, GitHub) — not the **local-alias** group (Dropbox, Google Drive shortcuts, local-sync tools).
- Within the single-shared-name group, the *who can rename* axis splits cleanly: Slack, Notion, Trello, and WhatsApp/Signal default to **egalitarian** (any member/editor); Teams, Discord, and GitHub default to **privileged** (owner/admin-role only).
- The privileged systems are guarding against a specific cost: once a rename is shared, it ripples to every other member's view. Restricting who can trigger that ripple limits how disruptive one member's unilateral action can be to everyone else.
- The app's pod model, however, has no privileged creator/admin tier for any other content action — app-behavior.md's Write Permissions section already makes notes, files, and chat freely editable by anyone in the pod. Introducing a creator-only restriction *just* for renaming would be a new asymmetry with no precedent elsewhere in the model.

## Decision

The app adopts the **egalitarian** model: any member of a pod can rename it, matching **Slack**'s and **Notion**'s default behavior, rather than restricting the action to the pod's creator the way **Microsoft Teams**, **Discord**, and **GitHub** do by default. This keeps renaming consistent with how every other pod-content operation already works in the app, rather than introducing a privilege tier that exists nowhere else in the model.

See app-behavior.md's "Naming, Renaming, and Sharing" section (under Pod Management) for the documented behavior this decision produced.

## Follow-on: the two-member exception

Applying the egalitarian, single-shared-name model uniformly to every pod — including a two-member pod — turned out to contradict a piece of behavior the model already had: on first receipt of a two-member pod, the recipient's app deliberately does *not* adopt the creator's own name; it auto-generates a name from the recipient's own side instead, precisely because the creator's name is "naturally centered on their own perspective" and would be a poor fit for the recipient. If renames still propagated to everyone after that first-receipt divergence, the very next rename on either side would silently overwrite the other member's perspective-fit name, defeating the reason the divergence exists at all.

The two-member case is different in kind from the group case this note otherwise covers: a pod with three or more members is a genuine shared group identity, like a Slack channel, with no single "other side" to name from — the egalitarian shared-name model fits it cleanly, same as Slack/Notion/Trello. A two-member pod, by contrast, is an asymmetric dyad — each member's name for it naturally reflects their own view of the *other* party, and there's no one name that correctly fits both perspectives simultaneously. That's the same reasoning the model already applied, just once, at first receipt; the fix generalizes it.

**Decision:** for two-member pods only, the name is not shared/synced content at all — each member is independently responsible for the name on their own side, in both directions, for the life of the pod. The creator's own name is whatever they set it to; the recipient's starts from the existing first-receipt auto-generated name; either may be freely renamed afterward, but a rename never propagates to the other member's copy. Single-member pods and pods with three or more members are unaffected and keep the egalitarian shared-name model described above.

See app-behavior.md's "Naming, Renaming, and Sharing" section (under Pod Management; the "Exception: bare two-member pods" paragraph) for the documented behavior this decision produced.
