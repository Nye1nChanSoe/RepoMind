# Retrieval: Plans

## Current Status

- implemented for hybrid reranking, repo-aware file-role biasing, diversity-aware selection, neighbor expansion, and compact context formatting

## Planned Work

- add a retrieval confidence signal
- add better failure handling and diagnostics around empty results
- allow user control over retrieved-file selection before generation
- add repo-profile-aware retrieval boosting
- expose retrieval diagnostics and scoring signals in the UI
- consider cross-file expansion beyond same-file neighbors
- reduce reliance on generic role heuristics with stronger repo-shape signals
- make retry retrieval smarter with import- and symbol-aware follow-up queries
