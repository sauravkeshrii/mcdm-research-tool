# Example 2: Project Selection

## Problem Description
A company needs to select the best project from 4 alternatives based on 4 criteria.

## Decision Matrix

| Alternative | Cost ($K) | Time (months) | Quality (1-10) | Risk (1-5) |
|-------------|-----------|---------------|----------------|------------|
| Project A   | 100       | 12            | 7              | 3          |
| Project B   | 150       | 8             | 9              | 2          |
| Project C   | 120       | 10            | 8              | 4          |
| Project D   | 90        | 15            | 6              | 5          |

## Criteria Information

- **Cost**: Cost (lower is better)
- **Time**: Cost (lower is better)
- **Quality**: Benefit (higher is better)
- **Risk**: Cost (lower is better)

**Criteria Types:** `[-1, -1, 1, -1]`

## How to Run

```bash
.venv/bin/python mcdm_calculator/calculator.py \
  mcdm_calculator/verification/examples/example2_projects.csv \
  --weights critic \
  --ranking topsis \
  --types "-1,-1,1,-1" \
  --verbose
```

## Expected Behavior

- **Project B** should rank high (best quality, low time, acceptable cost)
- **Project D** should rank low (worst quality, highest time, highest risk)
