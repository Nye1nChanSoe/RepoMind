# Ingestion: Special Notes For Agent

- keep ingestion limited to repository acquisition and file discovery
- do not move chunking or language-parsing logic into this layer
- if file support changes, update `utils/languages.py` and ingestion tests together
- notebook support is planned but not implemented, so do not document it as live behavior
