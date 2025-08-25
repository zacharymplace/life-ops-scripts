# ADR-001: Use ADR Format for Design Decisions

**Date:** 2025-08-24
**Status:** Accepted

---

## Context

We want a lightweight, consistent way to record design decisions for this project.
Tracking decisions makes it easier to onboard future contributors (including future Z$), review why choices were made, and ensure governance over time.

---

## Decision

We will use the **Architecture Decision Record (ADR) format** for all notable technical or process decisions.
ADRs will be stored in `docs/decisions/` and named sequentially: `ADR-XXX-title.md`.

---

## Consequences

- ✅ Transparent record of design choices over time.
- ✅ Easier to revisit/reverse decisions if needed.
- ⚠️ Requires discipline to maintain ADRs as the project evolves.
- 🔄 Future ADRs may supersede earlier ones.

---

## Alternatives Considered

- **No formal process** → Risk of losing context on decisions.
- **Heavyweight specs/docs** → Too much overhead for a personal project.

---

## References

- <https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions>
- <https://adr.github.io/>
