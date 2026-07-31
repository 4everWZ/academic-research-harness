# Claim Ledger

Create entries only for material claims or unresolved evidence risks.

## [Claim]

- **Intended use:** [section or conclusion]
- **Evidence:** [citation keys, code/config references, or result provenance]
- **Implementation provenance:** [revision, entrypoint, active overrides, reachability, and present/enabled/executed status, or not applicable]
- **Author decision:** [none, pending, or the explicitly approved framing/method choice]
- **Decision authority/date:** [user direction and date, or pending]
- **Status:** supported | partial | unsupported | speculative | unverified
- **Ledger audit:** pending | verified
- **Audit date/evidence snapshot:** [date and source or artifact revisions checked, or pending]
- **Required action:** [verification, revision, decision, or none]
- **Public handling:** direct | scoped | limitations | omit | pending decision

Never infer approval or verification. `direct` requires `supported` status and
a `verified` audit. Resolve contradictory fields before using the entry.
