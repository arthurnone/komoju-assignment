# Gilded Rose – Implemented in Python and Ruby

## Introduction

To demonstrate both my problem-solving ability and adaptability, I implemented the Gilded Rose assignment in **both Python and Ruby**.

- Python is my primary language.
- Ruby was used additionally to align with **KOMOJU’s technical stack** and show my readiness to contribute in a Ruby environment.

## Goals and Focus

- ✅ Correctly implement **all business rules** as described in the specification
- ✅ Add **detailed logging** for tracking `sell_in` and `quality` changes
- ✅ Write **comprehensive test coverage** (edge cases, regression, boundary conditions)
- ✅ Set up **CI pipelines** for both implementations using GitHub Actions

## Design Principles

- **Language-agnostic correctness**: Both implementations follow the same core logic structure, adapted to idiomatic usage in each language.
- **Separation of concerns**: Update logic for different item types is modularized (`update_aged_brie`, `update_backstage_pass`, etc.).
- **Avoid overengineering**: I intentionally avoided complex abstractions like class hierarchies or strategy patterns, to keep the logic approachable and focused on correctness.

## Highlights

- Supports all edge cases and item types:
  - `"Aged Brie"` increasing in quality over time
  - `"Backstage passes"` dropping to 0 after the concert
  - `"Sulfuras"` remaining unchanged with constant quality of 80
  - `"Conjured"` items degrading twice as fast, combined with other types
- Quality is clamped between 0 and 50 (except `"Sulfuras"`).
- **Logging** is added in both versions to monitor item state transitions.
- **CI** is configured separately for Python and Ruby:
  - Python: `unittest` + `coverage`
  - Ruby: `RSpec` + `SimpleCov`

## Final Notes

> I chose to implement this project in both Python and Ruby not just to meet the technical requirement, but to show:
> - My ability to **translate complex business rules into clean, maintainable code**
> - My comfort with **professional engineering practices** (tests, logging, CI/CD)
> - My flexibility in working across **multiple programming languages** in real-world production contexts

Please feel free to ask if you'd like a walkthrough of either version during the interview.
