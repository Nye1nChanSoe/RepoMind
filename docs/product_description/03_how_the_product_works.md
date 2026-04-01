# /docs/product_description/03_how_the_product_works.md

## Default User Flow

1. The user gives RepoMind a repository and a request.
2. RepoMind finds the code most likely related to that request.
3. RepoMind explains what the current code does.
4. RepoMind proposes a minimal plan.
5. RepoMind produces a draft diff and explanation.

## What The User Receives

The output should feel like a compact review packet:
- relevant files
- current-state understanding
- proposed implementation plan
- proposed code changes
- explanation of the change

## How Value Is Created

RepoMind creates value by reducing search and decision overhead.

Instead of asking the user to manually inspect a large repository, it narrows attention to the code that most likely matters and turns that into a structured proposal.

## Product-Level Workflow Principles

- retrieval before reasoning
- reasoning before generation
- explanation before trust
- minimal change before broad rewrite
