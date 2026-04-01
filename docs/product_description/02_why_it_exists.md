# /docs/product_description/02_why_it_exists.md

## The Problem

Developers often lose time before they write any code.

The hard part is usually not typing the patch. The hard part is:
- finding the right files
- understanding the current behavior
- deciding the smallest correct change

This is especially painful in unfamiliar repositories.

## Why Existing Tools Are Not Enough

Plain search tools can find text, but they do not explain what matters.

General coding agents can attempt end-to-end changes, but they often:
- widen scope too quickly
- hide their reasoning
- touch more files than necessary

## Why RepoMind Exists

RepoMind exists to reduce the cost of first-pass code understanding and change planning.

It is meant to answer:
- where should I look
- what does this code currently do
- what is the smallest reasonable change

## Product Bet

The core product bet is that many useful code-assistance tasks can be solved well enough by:
- retrieving a small amount of relevant code
- reasoning in stages
- keeping outputs structured and reviewable
