# Iteration 03: Objective

## Goal

Make simple component tuning easier to change without code edits.

## Problems Targeted

- changing chunk sizes or retrieval limits required direct code edits
- small tuning changes consumed unnecessary implementation context
- there was no single place to manually adjust component defaults

## Intended Outcome

- per-component JSON files hold simple tuning values
- code keeps safe defaults and fallback behavior
- future tuning iterations can happen with less code churn
