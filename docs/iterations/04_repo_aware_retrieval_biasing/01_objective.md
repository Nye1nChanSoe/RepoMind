# Iteration 04: Objective

## Goal

Reduce cases where retrieval is dominated by docs, tutorials, tests, and dependency/vendor code when the requested change likely belongs in implementation code.

## Problems Targeted

- test, tutorial, and dependency/vendor files often share the same request vocabulary as the core implementation
- semantic retrieval can overselect examples and underselect framework internals
- same-file neighbor expansion does not help when the selected files are the wrong kind of files

## Intended Outcome

- retrieval recognizes basic file roles such as implementation, test, docs, and dependency code
- implementation files get a better chance to appear in the final context set
- docs/tests/dependency code can still help, but they should not crowd out likely implementation code
