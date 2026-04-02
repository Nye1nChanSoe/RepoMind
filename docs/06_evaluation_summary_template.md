# 06 Evaluation Summary Template (Across 5 Repositories)

Use this after completing all per-repo reports.

---

## 1) Evaluation Scope

- Number of repositories: 5
- Selection rationale: Heterogeneous repository set to test inference robustness across project styles and complexity
- Common prompt suite version: Single feature-request prompt per repo (same wording reused)
- Evaluation window: 2026-04-02 to TBD
- Evaluator: nyeinchan

## 2) Repository Set

| # | Repository | Type | Size | Stack | Notes |
|---|------------|------|------|-------|-------|
| 1 | evanw/esbuild | Tooling (bundler/minifier) | Large | Go | Repo 1 complete |
| 2 | markedjs/marked | Library (markdown parser/renderer) | Medium | TypeScript/JS | Repo 2 complete |
| 3 |            |      |      |       |       |
| 4 |            |      |      |       |       |
| 5 |            |      |      |       |       |

## 3) Scorecard Comparison (1-5)

| Repository | Correctness | Depth | Actionability | Hallucination Control | Confidence Calibration | Overall |
|------------|-------------|-------|---------------|------------------------|------------------------|---------|
| evanw/esbuild | 2 | 2 | 2 | 1 | 2 | 1.8 |
| markedjs/marked | 3 | 2 | 3 | 2 | 3 | 2.6 |
| Repo 3     |             |       |               |                        |                        |         |
| Repo 4     |             |       |               |                        |                        |         |
| Repo 5     |             |       |               |                        |                        |         |

## 4) Ranking

1. 
2. 
3. 
4. 
5. 

## 5) Cross-Repo Findings

### 5.1 Where Inference Is Strong

- 

### 5.2 Where Inference Is Weak

- 

### 5.3 Common Hallucination Patterns

- 

### 5.4 Confidence Calibration Patterns

- 

## 6) Prompt-Level Performance

| Prompt | Success Pattern | Failure Pattern | Suggested Prompt Change |
|--------|------------------|-----------------|--------------------------|
| A      |                  |                 |                          |
| B      |                  |                 |                          |
| C      |                  |                 |                          |
| D      |                  |                 |                          |
| E      |                  |                 |                          |

## 7) Reliability Bands

- Strong fit repo types:
- Moderate fit repo types:
- Weak fit repo types:

## 8) Final Conclusion

- Overall inference level across tested repos:
- Confidence in deployment readiness:
- Recommended operational guardrails:
- Go/No-go recommendation:

## 9) Next Iteration Plan

1. Prompt changes to test:
2. Additional repo types to include:
3. Metrics to add (if any):
4. Decision checkpoint date:
