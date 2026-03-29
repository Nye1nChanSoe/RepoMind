# /docs/use_cases/03_failure_modes.md

## Weak Retrieval

Symptoms:
- retrieved chunks are adjacent but not actually relevant
- the plan sounds generic
- generated diff edits the wrong file

Expected system behavior:
- surface the retrieved files clearly
- avoid overconfident language
- allow debugging from intermediate outputs

## Ambiguous Request

Symptoms:
- the request could map to multiple features or layers

Expected system behavior:
- produce a constrained plan if one interpretation is clearly dominant
- otherwise return a limitation or ask for narrower scope in future iterations

## Unsupported Code Structure

Symptoms:
- parser cannot extract symbols
- unusual project layout weakens retrieval

Expected system behavior:
- fall back to line-based chunking
- continue with reduced confidence

## Invalid Generation Output

Symptoms:
- malformed JSON
- missing fields
- diff without corresponding original or modified blocks

Expected system behavior:
- validate output
- retry or return a structured error instead of broken UI data
