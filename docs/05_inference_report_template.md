# 05 Inference Report Template (Per Repository)

Use this template once per repository.

---

## 1) Repository Metadata

- Repository name:
- Repository URL:
- Commit/branch evaluated:
- Repo size estimate (small/medium/large):
- Primary language(s):
- Domain type (library/service/app/framework/tooling):
- Evaluation date:
- Evaluator:

## 2) Evaluation Setup

- Access mode (local clone/fork/upstream):
- Context provided to agent (if any):
- Time budget:
- Constraints used:

## 3) Prompt Suite Used

Use the same prompts across all repositories.

### Prompt A: Architecture Inference

```
Explain this repository's architecture: core modules, data flow, runtime boundaries, and dependency directions. Include uncertain areas explicitly.
```

### Prompt B: Domain/Business Inference

```
Infer the product/domain purpose and intended users from this codebase. Distinguish direct evidence from assumptions.
```

### Prompt C: Risk and Bug Hotspot Inference

```
Identify likely risk areas and bug hotspots in this repo, with reasons tied to specific files or patterns.
```

### Prompt D: Missing Docs/Tests Inference

```
Infer which documentation and tests are most missing or weak, and prioritize the top gaps.
```

### Prompt E: First 3 Improvements

```
Recommend the first 3 high-impact improvements for this repository, each with rationale, effort estimate, and expected outcome.
```

## 4) Raw Outputs

- Output A:
- Output B:
- Output C:
- Output D:
- Output E:

## 5) Validation Against Ground Truth

### 5.1 What Was Correct

- 

### 5.2 What Was Partially Correct

- 

### 5.3 What Was Incorrect (Hallucinations/Errors)

- 

## 6) Scoring (1-5)

### 6.1 Correctness

- Score:
- Justification:

### 6.2 Depth

- Score:
- Justification:

### 6.3 Actionability

- Score:
- Justification:

### 6.4 Hallucination Control

- Score:
- Justification:

### 6.5 Confidence Calibration

- Score:
- Justification:

## 7) Confidence vs Reality

- Where confidence matched actual certainty:
- Where confidence was too high:
- Where confidence was too low:

## 8) Final Repo Score

- Weighted total (optional formula):
- Overall score:
- Pass/Needs improvement:

## 9) Repo Conclusion

- Inference level reached (surface/moderate/deep):
- Most reliable inference category:
- Weakest inference category:
- Recommendation for production use on this repo:

