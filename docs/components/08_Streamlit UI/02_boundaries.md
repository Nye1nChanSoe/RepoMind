# Streamlit UI: Boundaries

## Owns

- user input capture for repo URL, request, and top-k
- pipeline orchestration trigger from UI interaction
- stage progress and failure messaging
- rendering final structured output for users

## Does Not Own

- repository cloning logic
- file discovery and chunking logic
- embedding/index storage implementation
- retrieval ranking implementation
- LLM reasoning and JSON parsing internals

## Upstream And Downstream

- upstream components: Generate (terminal reasoning output)
- downstream consumer: end user in Streamlit interface

