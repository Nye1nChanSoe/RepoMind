# Streamlit UI: Special Notes For Agent

- keep UI orchestration logic readable and stage-labeled for debugging
- preserve current failure transparency; do not swallow exceptions silently
- avoid adding hidden side effects in UI handlers
- keep top-k controls and request input explicit and user-editable
- if output shape changes, update both rendering blocks and component docs

