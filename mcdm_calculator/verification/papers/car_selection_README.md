# Car Selection - TOPSIS Example

## Source
Standard TOPSIS numerical example widely used in academic literature and educational materials for demonstrating the TOPSIS methodology.

**Based on:** Common pedagogical example found in MCDM textbooks and tutorials
**Method:** TOPSIS (Hwang & Yoon, 1981)
**Purpose:** Educational verification of TOPSIS implementation

**Original TOPSIS Method:**
```
Hwang, C. L., & Yoon, K. (1981). Multiple Attribute Decision Making: Methods and Applications. 
Springer-Verlag, New York.
```

## Problem Description
Choose the best car among three alternatives based on four criteria.

## Decision Matrix

| Alternative | Fuel Efficiency (km/L) | Price ($) | Safety Rating (1-10) | Comfort (1-10) |
|-------------|------------------------|-----------|----------------------|----------------|
| Car A       | 15                     | 25,000    | 8                    | 7              |
| Car B       | 12                     | 20,000    | 9                    | 8              |
| Car C       | 14                     | 22,000    | 7                    | 9              |

## Criteria Information

- **Fuel Efficiency**: Benefit (higher is better)
- **Price**: Cost (lower is better)
- **Safety Rating**: Benefit (higher is better)
- **Comfort**: Benefit (higher is better)

**Criteria Types:** `[1, -1, 1, 1]`

**Weights:** `[0.25, 0.30, 0.20, 0.25]`

## Expected Results (from Paper)

### Step 1: Normalized Matrix (Vector Normalization)
```
Car A: [0.6319, 0.6436, 0.5744, 0.5026]
Car B: [0.5048, 0.5148, 0.6462, 0.5744]
Car C: [0.5890, 0.5663, 0.5026, 0.6462]
```

### Step 2: Weighted Normalized Matrix
```
Car A: [0.1580, 0.1931, 0.1149, 0.1257]
Car B: [0.1262, 0.1544, 0.1292, 0.1436]
Car C: [0.1472, 0.1699, 0.1005, 0.1616]
```

### Step 3: Ideal Solutions
```
A* (Ideal):      [0.1580, 0.1544, 0.1292, 0.1616]
A- (Anti-Ideal): [0.1262, 0.1931, 0.1005, 0.1257]
```

### Step 4: Separation Measures
```
S+ (Distance to Ideal):
  Car A: 0.0547
  Car B: 0.0365
  Car C: 0.0344

S- (Distance to Anti-Ideal):
  Car A: 0.0349
  Car B: 0.0514
  Car C: 0.0476
```

### Step 5: Closeness Coefficient
```
Car A: 0.3895
Car B: 0.5847
Car C: 0.5805
```

### Final Ranking
```
1. Car B (0.5847)
2. Car C (0.5805)
3. Car A (0.3895)
```

## How to Run

```bash
cd /media/NewVolume/mcdm.ai/mcdm-research-tool

# Run with verbose mode to see all steps
.venv/bin/python mcdm_calculator/calculator.py \
  mcdm_calculator/verification/papers/car_selection_topsis.csv \
  --weights manual \
  --manual-weights "0.25,0.30,0.20,0.25" \
  --ranking topsis \
  --types="1,-1,1,1" \
  --verbose

# Compare with expected results
.venv/bin/python mcdm_calculator/calculator.py \
  mcdm_calculator/verification/papers/car_selection_topsis.csv \
  --weights manual \
  --manual-weights "0.25,0.30,0.20,0.25" \
  --ranking topsis \
  --types="1,-1,1,1" \
  --compare mcdm_calculator/verification/papers/car_selection_expected.json \
  --tolerance 0.01
```

## Verification

This example is used to verify that our TOPSIS implementation matches the standard academic formulation. All intermediate steps should match the values shown above within rounding tolerance.
