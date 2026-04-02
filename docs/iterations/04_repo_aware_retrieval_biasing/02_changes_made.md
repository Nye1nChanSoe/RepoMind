# Iteration 04: Changes Made

## Retrieval Changes

- classify file paths into simple roles such as implementation, test, docs, dependency, and config
- apply score priors by file role during retrieval reranking
- reserve part of the final retrieved set for implementation files when available
- add lightweight cross-file bridging so strong doc/test/dependency matches can help surface related implementation chunks
- expand ingestion skip directories for common dependency/vendor folders such as `vendor`, `third_party`, and `bower_components`

## UI Changes

- make blocked-context notes more specific when retrieval is dominated by docs/tests/dependency files

## Configuration Changes

- add retrieval config knobs for file-role priors, implementation-result minimums, and a dependency-role penalty
