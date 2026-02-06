# Verification Guide

This directory contains examples and tools to verify the correctness of MCDM implementations.

## Directory Structure

```
verification/
├── examples/          # Worked examples with data and expected results
│   ├── example1_phones.csv
│   ├── example1_README.md
│   ├── example1_expected.json
│   ├── example2_projects.csv
│   └── example2_README.md
└── papers/           # Examples from academic papers (add your own)
```

## How to Verify Your Implementation

### Method 1: Run Examples with Verbose Mode

```bash
cd /media/NewVolume/mcdm.ai/mcdm-research-tool

# Run with detailed step-by-step output
.venv/bin/python mcdm_calculator/calculator.py \
  mcdm_calculator/verification/examples/example1_phones.csv \
  --weights merec \
  --ranking topsis \
  --types "-1,1,1,1" \
  --verbose
```

This will show:
- Original decision matrix
- Normalized matrix (each step)
- Weighted matrix
- Ideal/Anti-ideal solutions
- Distance calculations
- Final scores and ranking

### Method 2: Compare with Expected Results

```bash
# Compare your results with known correct values
.venv/bin/python mcdm_calculator/calculator.py \
  mcdm_calculator/verification/examples/example1_phones.csv \
  --weights merec \
  --ranking topsis \
  --types "-1,1,1,1" \
  --compare mcdm_calculator/verification/examples/example1_expected.json \
  --tolerance 0.05
```

This will:
- Run the calculation
- Compare weights, scores, and rankings with expected values
- Show differences and pass/fail status
- Use specified tolerance for numerical comparison

### Method 3: Add Your Own Paper Examples

1. Create a CSV file with the decision matrix from a paper
2. Create a JSON file with expected results
3. Run comparison mode

**Example JSON format:**
```json
{
  "description": "Paper Title - Table X",
  "method": "MEREC + TOPSIS",
  "weights": [0.25, 0.30, 0.20, 0.25],
  "scores": [0.65, 0.45, 0.80, 0.55],
  "ranking": [2, 4, 1, 3],
  "notes": "Any additional notes"
}
```

## Included Examples

### Example 1: Smartphone Selection
- **File:** `example1_phones.csv`
- **Criteria:** Price (cost), Storage (benefit), Camera (benefit), Looks (benefit)
- **Methods:** MEREC + TOPSIS
- **Expected:** `example1_expected.json`

### Example 2: Project Selection
- **File:** `example2_projects.csv`
- **Criteria:** Cost (cost), Time (cost), Quality (benefit), Risk (cost)
- **Methods:** Any combination

## Verification Checklist

When verifying an MCDM implementation, check:

- [ ] **Weights sum to 1.0** (within floating-point precision)
- [ ] **Normalization is correct** (check range and formula)
- [ ] **Ideal solutions are correct** (max for benefit, min for cost in TOPSIS)
- [ ] **Scores are in valid range** (0-1 for TOPSIS, 0-1 for VIKOR)
- [ ] **Ranking makes logical sense** (better alternatives rank higher)
- [ ] **Results match published papers** (within rounding tolerance)
- [ ] **Edge cases handled** (zero values, identical values, etc.)

## Common Issues

### Numerical Precision
- Use tolerance of 0.01-0.05 when comparing with papers
- Papers often round to 2-4 decimal places
- Different software may have slight variations

### Formula Variations
- Some papers use slightly different normalization methods
- Check the FORMULAS.md file for exact implementations
- Document any deviations in your comparison JSON

### Data Format
- Ensure CSV has alternatives as rows, criteria as columns
- First column should be alternative names (will be used as index)
- No missing values

## Adding New Verification Cases

To add a new verification case from a research paper:

1. **Extract the decision matrix** from the paper
2. **Create CSV file:** `paperName_tableX.csv`
3. **Create README:** `paperName_README.md` with:
   - Paper citation
   - Table/example number
   - Criteria descriptions
   - Expected results
4. **Create JSON:** `paperName_expected.json` with expected values
5. **Test:** Run with `--compare` flag

## Tips for Researchers

1. **Start with simple examples** (3-4 alternatives, 3-4 criteria)
2. **Verify step-by-step** using `--verbose` mode
3. **Cross-check with multiple sources** if possible
4. **Document your verification** in the README files
5. **Share your verified examples** with the community

## Questions?

If you find discrepancies:
1. Check the FORMULAS.md for exact implementation
2. Verify your input data format
3. Check if the paper uses a variation of the method
4. Try adjusting the tolerance
5. Use verbose mode to identify where differences occur
