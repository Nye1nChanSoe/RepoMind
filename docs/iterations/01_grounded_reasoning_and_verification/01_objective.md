# Iteration 01: Objective

## Goal

Reduce hallucination compounding across the current staged pipeline without redesigning the whole system.

## Problems Targeted

- understanding output was plain English and did not separate facts from inference
- planning relied on summary text instead of direct code evidence
- generated output could drift beyond retrieved context with no local warning
- the UI did not expose when a result was weakly supported

## Intended Outcome

- later stages receive evidence-carrying intermediate data
- unsupported or weakly supported results become visible
- the system becomes safer to iterate on before deeper retrieval work
