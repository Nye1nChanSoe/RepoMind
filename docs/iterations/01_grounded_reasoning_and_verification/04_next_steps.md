# Iteration 01: Next Steps

## Highest-Value Follow-Up Work

1. Add hybrid retrieval with lexical, symbol, and path-aware boosts.
2. Add neighbor expansion so matched symbols bring along nearby code.
3. Add a lightweight repo-profile phase before retrieval and prompting.
4. Expand chunk metadata to include file-role signals such as tests, config, and entrypoints.

## Why These Come Next

- the first iteration reduces hallucination compounding inside the reasoning pipeline
- the next biggest gap is still retrieval quality
- repo awareness will improve behavior across different repository shapes

## Exit Criteria For Iteration 02

- retrieval returns more precise and more diverse context
- outputs rely less on weak cross-file inference
- evaluation runs show fewer unsupported file suggestions
