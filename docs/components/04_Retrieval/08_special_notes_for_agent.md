# Retrieval: Special Notes For Agent

- keep retrieval formatting compact because it is passed directly to LLM prompts
- if context headers change, update tests and prompt assumptions together
- do not move planning logic into retrieval
- treat zero-result behavior as a product decision, not just an implementation detail
