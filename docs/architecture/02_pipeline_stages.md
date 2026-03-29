# /docs/architecture/02_pipeline_stages.md

## Stage 1: Ingestion

Responsibility:
- clone repository
- identify supported source files
- skip generated, vendor, and oversized files

Current implementation:
- supports extension-based source file discovery
- does not implement `.ipynb` notebook ingestion yet

Output:
- local repository path
- list of candidate source files

## Stage 2: Chunking

Responsibility:
- split code into meaningful chunks
- attach metadata needed for retrieval and display

Preferred behavior:
- AST-level chunks for supported languages
- line-based fallback when AST parsing is unavailable

Current implementation:
- AST path for Python, JavaScript, TypeScript, and Go
- line-based fallback for other detected source files
- notebook chunking is planned but not implemented yet

Output:
- chunk objects with content and metadata

## Stage 3: Embedding and Indexing

Responsibility:
- generate embeddings locally
- store vectors, content, and metadata in ChromaDB

Output:
- queryable collection keyed by repository or session

Current implementation:
- one Chroma collection per repository URL hash in the Streamlit app
- the collection is cleared and rebuilt on each run

## Stage 4: Retrieval

Responsibility:
- embed the user request
- retrieve top-k relevant chunks
- format compact context for downstream LLM calls

Output:
- ordered chunk list
- formatted context string

Current implementation:
- formatted context is used for the understand step
- formatted context is reused for the generate step
- the plan step currently uses understanding plus the user request

## Stage 5: Understand

Responsibility:
- explain current code behavior
- connect related files and functions
- avoid suggesting changes yet

Output:
- plain-English understanding summary

Current implementation:
- powered by `MODEL_UNDERSTAND`

## Stage 6: Plan

Responsibility:
- map the request to specific files and functions
- keep the approach minimal
- return structured JSON

Output:
- plan entries
- brief rationale

Current implementation:
- powered by `MODEL_PLAN`
- expected to return JSON and parsed locally

## Stage 7: Generate

Responsibility:
- propose code changes based on the plan
- keep outputs aligned with retrieved context
- produce machine-readable structured output

Output:
- per-file original and modified code
- unified diffs
- review-style explanation

Current implementation:
- powered by `MODEL_GENERATE`
- explanation is returned as part of the generate step response
- diff text is accepted from the model or generated locally as a fallback
