# 05 Inference Report Template (Per Repository)

Use this template once per repository.

This template is for the actual evaluation flow:
- choose one repository
- paste one real feature request or GitHub issue
- run the RepoMind pipeline with retrieved repo context
- have an external LLM judge evaluate the pipeline response

---

## 1) Repository

- Repository name:
- Repository URL:
- Commit/branch evaluated:
- Repo size estimate (small/medium/large):
- Primary language(s):
- Evaluation date:

## 2) Input Used

### User Request (Copied As-Is)

```text
Paste the exact feature request or issue text here.
```

### Pipeline Run Settings

- Top-K chunks:
- Any extra constraints:

## 3) Pipeline Output

### Relevant Files

- 

### Understanding

```text
Paste the pipeline understanding output here.
```

### Plan

```text
Paste the pipeline plan output here.
```

### Proposed Changes

```text
Paste the pipeline proposed changes summary here.
```

### Explanation

```text
Paste the pipeline explanation here.
```

### Verifier Warnings

- 

## 4) External Judge Setup

- Judge model/system:
- Judge role: external evaluator with no relation to RepoMind
- Evaluation method: review the request, retrieved context summary, and pipeline response

## 5) Judge Findings

### What The Pipeline Got Right

- 

### What The Pipeline Got Wrong

- 

### Missing Context Or Unsupported Assumptions

- 

## 6) Scoring (1-5)

### Correctness

- Score:
- Why:

### Grounding

- Score:
- Why:

### Actionability

- Score:
- Why:

### Hallucination Control

- Score:
- Why:

### Confidence Calibration

- Score:
- Why:

## 7) Final Verdict

- Overall score:
- Inference level reached (surface/moderate/deep):
- Would this be safe to use as a first draft on this repo?:
- Main reason for the verdict:

## 8) Notes For Next Iteration

- What would most improve results on this repo:
- Prompt or retrieval issue noticed:
- Worth retesting after the next system iteration?:

