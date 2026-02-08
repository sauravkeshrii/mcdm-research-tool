# MCDM Calculator - Research-Ready Tool

[![Verification Status](https://img.shields.io/badge/Verification-Passed-brightgreen)](VERIFICATION_REPORT.md)
[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-Academic-orange.svg)](#license)

A comprehensive, **verified** Multi-Criteria Decision Making (MCDM) calculator designed for researchers, students, and practitioners. This tool implements multiple MCDM methods with **mathematical accuracy verified against published academic examples**.

## 🎯 Why This Tool?

- ✅ **Verified Implementation** - Tested against standard academic examples (see [VERIFICATION_REPORT.md](VERIFICATION_REPORT.md))
- 📚 **Proper Citations** - Full academic attribution to original researchers (see [CITATIONS.md](CITATIONS.md))
- 🔍 **Transparent Calculations** - Verbose mode shows every step
- 🧪 **Research-Ready** - Compare your results with published papers
- 📖 **Complete Documentation** - Exact formulas, examples, and guides

> 📚 **New to this project?** See [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md) for a complete guide to all documentation files.

> 🚀 **Want to get started quickly?** Jump to [Quick Start](#quick-start) or check [QUICK_REFERENCE.md](QUICK_REFERENCE.md).

---
## Screenshots

![Dashboard]((https://github.com/sauravkeshrii/mcdm-research-tool/blob/main/1.png))
![Results]((https://github.com/sauravkeshrii/mcdm-research-tool/blob/main/2.png))

---
## Features

### 🔢 Weighting Methods (Objective & Subjective)
- **MEREC** - Method based on Removal Effects of Criteria (2021)
- **Entropy** - Information entropy-based weighting (Shannon, 1948)
- **CRITIC** - Criteria Importance Through Intercriteria Correlation (1995)
- **Equal Weights** - Uniform distribution
- **Manual Weights** - User-defined weights

### 📊 Ranking Methods
- **TOPSIS** - Technique for Order Preference by Similarity to Ideal Solution (1981)
- **VIKOR** - Multicriteria Optimization and Compromise Solution (1979/2004)
- **MAIRCA** - Multi-Attributive Border Approximation area Comparison (2014)

### 🔬 Research Features

✅ **Verbose Mode**
- Step-by-step calculations with formulas
- All intermediate matrices displayed
- Full transparency for academic verification

✅ **Comparison Mode**
- Compare your results with expected values from papers
- Configurable numerical tolerance
- Detailed difference reporting with ✓/✗ indicators

✅ **Verification Examples**
- Real examples from academic literature
- Expected results included
- Ready-to-run test cases

✅ **Complete Documentation**
- Exact mathematical formulas ([FORMULAS.md](mcdm_calculator/FORMULAS.md))
- Academic citations ([CITATIONS.md](CITATIONS.md))
- Worked examples with step-by-step solutions
- Verification guide for researchers

---

### 🖥️ New UI Interface (Streamlit)

✅ **Interactive Dashboard**
- Browser-based GUI for easy data entry
- Interactive tables and visualizations
- No coding required

## 📑 Table of Contents

- [Quick Start](#quick-start)
  - [Launch UI (New!)](#launch-ui)
  - [Installation](#installation)
  - [Basic Usage](#basic-usage)
  - [Verbose Mode](#verbose-mode-detailed-steps)
  - [Comparison Mode](#comparison-mode-verify-against-papers)
- [Project Structure](#project-structure)
- [Input Data Format](#input-data-format)
- [Criteria Types](#criteria-types)
- [Examples](#examples)
- [For Researchers](#for-researchers)
- [Command-Line Options](#command-line-options)
- [Output](#output)
- [Mathematical Methods](#mathematical-methods)
- [Academic Citations & Credits](#academic-citations--credits)
- [License](#license)
- [Contributing](#contributing)

---

## Quick Start

### Launch UI (New!)

Run the interactive web interface:

```bash
# Install dependencies
pip install -r requirements.txt

# Launch UI
streamlit run app.py
```

### Installation

```bash
cd /media/NewVolume/mcdm.ai/mcdm-research-tool

# Activate virtual environment
source .venv/bin/activate

# Install dependencies (if not already installed)
pip install numpy pandas
```

### Basic Usage

```bash
# Simple calculation
python mcdm_calculator/calculator.py data.csv \
  --weights merec \
  --ranking topsis \
  --types "-1,1,1,1"
```

### Verbose Mode (Detailed Steps)

```bash
python mcdm_calculator/calculator.py data.csv \
  --weights merec \
  --ranking topsis \
  --types "-1,1,1,1" \
  --verbose
```

This shows:
- Original decision matrix
- Normalized matrix (step-by-step)
- Weighted matrix
- Ideal/Anti-ideal solutions
- Distance calculations
- Final scores and ranking

### Comparison Mode (Verify Against Papers)

```bash
python mcdm_calculator/calculator.py data.csv \
  --weights merec \
  --ranking topsis \
  --types "-1,1,1,1" \
  --compare expected_results.json \
  --tolerance 0.05
```

---

## 📂 Project Structure

### 📄 Root Directory
| File | Description |
|------|-------------|
| **`README.md`** | Main documentation hub containing usage guides, features, and quick start instructions. |
| **`app.py`** | **Streamlit UI Entry Point**. Launches the web-based interactive dashboard. |
| **`requirements.txt`** | List of Python dependencies (pandas, numpy, streamlit, openpyxl, matplotlib). |
| **`test_quick.py`** | specific automation script for quick verification of all methods. |
| **`DOCUMENTATION_INDEX.md`** | Navigation guide for all documentation files. |
| **`CITATIONS.md`** | Comprehensive list of academic papers and authentic citations for implemented methods. |
| **`VERIFICATION_REPORT.md`** | Detailed report proving the mathematical accuracy against standard academic examples (e.g., Car Selection). |
| **`IMPLEMENTATION_SUMMARY.md`** | Technical summary of implemented features, verbose modes, and research capabilities. |
| **`ATTRIBUTION_SUMMARY.md`** | Credits to original researchers and contributors. |

### 📦 `mcdm_calculator/` Package
This is the core logic package containing the mathematical engine.

| File/Dir | Description |
|----------|-------------|
| **`calculator.py`** | **CLI Entry Point**. Handles command-line arguments and executes the logic pipeline. |
| **`service.py`** | **API Layer**. Bridges the Streamlit UI with the Core Logic, handling data framing and response formatting. |
| **`FORMULAS.md`** | **Math Reference**. Contains exact LaTeX formulas for Normalization, Weighting, and Ranking methods. |
| **`core/`** | **Mathematical Engine**: |
| ├── `normalization.py` | Implements Vector, Min-Max, Linear, and Sum normalization techniques. |
| ├── `weighting.py` | Implements objective weighting methods: MEREC, Entropy, CRITIC. |
| └── `ranking.py` | Implements ranking algorithms: TOPSIS, VIKOR, MAIRCA. |
| **`verification/`** | Contains validated datasets (CSV) and JSON expected results for testing. |
| **`tests/`** | Unit tests ensuring system stability. |


---

## Input Data Format

CSV file with:
- First column: Alternative names (will be used as index)
- Other columns: Criteria values
- No missing values

**Example:**
```csv
Alternative,Price,Storage,Camera,Looks
Phone A,250,16,12,5
Phone B,200,16,8,3
Phone C,300,32,16,4
```

## Criteria Types

Specify whether each criterion is benefit (higher is better) or cost (lower is better):

```bash
--types "-1,1,1,1"
```

Where:
- `-1` or `cost` = Cost criterion (lower is better)
- `1` or `benefit` = Benefit criterion (higher is better)

You can also use words:
```bash
--types "cost,benefit,benefit,benefit"
```

## Examples

### Example 1: Smartphone Selection

```bash
python mcdm_calculator/calculator.py \
  mcdm_calculator/verification/examples/example1_phones.csv \
  --weights merec \
  --ranking topsis \
  --types="-1,1,1,1" \
  --verbose
```

### Example 2: Project Selection

```bash
python mcdm_calculator/calculator.py \
  mcdm_calculator/verification/examples/example2_projects.csv \
  --weights critic \
  --ranking vikor \
  --types="-1,-1,1,-1"
```

## For Researchers

### Verifying Your Implementation

1. **Use Verbose Mode** to see all intermediate steps
2. **Compare with Papers** using the comparison mode
3. **Check the Formulas** in `FORMULAS.md` to ensure they match your needs
4. **Add Your Own Examples** in the `verification/` folder

### Adding Paper Examples

1. Create CSV with decision matrix from paper
2. Create JSON with expected results:

```json
{
  "description": "Paper Title - Table X",
  "method": "MEREC + TOPSIS",
  "weights": [0.25, 0.30, 0.20, 0.25],
  "scores": [0.65, 0.45, 0.80, 0.55],
  "ranking": [2, 4, 1, 3]
}
```

3. Run with `--compare` flag to verify

### Documentation

- **`FORMULAS.md`**: Exact mathematical formulas for all methods
- **`verification/README.md`**: Complete verification guide
- **`verification/examples/`**: Worked examples with expected results

## Command-Line Options

```
positional arguments:
  data                  Path to input CSV file

optional arguments:
  -h, --help            Show help message
  --weights {merec,entropy,critic,equal,manual}
                        Weighting method (default: merec)
  --ranking {topsis,vikor,mairca}
                        Ranking method (default: topsis)
  --types TYPES         Criteria types (e.g., "-1,1,1,1")
  --manual-weights MANUAL_WEIGHTS
                        Manual weights if --weights=manual
  --verbose, -v         Show detailed step-by-step calculations
  --compare FILE        Compare with expected results from JSON
  --tolerance TOLERANCE
                        Tolerance for comparison (default: 0.01)
```

## Output

The calculator produces:
1. **Console output**: Results displayed in terminal
2. **CSV file**: `result_{ranking}_{weights}.csv` with detailed results

## Testing

Run the quick test to verify installation:

```bash
python test_quick.py
```

This tests all weighting and ranking methods with a sample dataset.

## Mathematical Methods

### Normalization
- Vector Normalization (for TOPSIS)
- Min-Max Normalization
- Linear Normalization (for MAIRCA)
- Sum Normalization (for Entropy)

### Weighting
- **MEREC**: Based on removal effects of criteria
- **Entropy**: Based on information entropy
- **CRITIC**: Based on correlation and standard deviation

### Ranking
- **TOPSIS**: Distance to ideal solution
- **VIKOR**: Compromise solution
- **MAIRCA**: Gap from theoretical rating

See `FORMULAS.md` for complete mathematical details.

## Academic Citations & Credits

This tool implements methods developed by pioneering researchers in Multi-Criteria Decision Making. We gratefully acknowledge their contributions:

### TOPSIS Method
**Original Developers:** Ching-Lai Hwang and Kwangsun Yoon

**Citation:**
```
Hwang, C. L., & Yoon, K. (1981). Multiple Attribute Decision Making: Methods and Applications. 
Springer-Verlag, New York.
```

### MEREC Method
**Original Developers:** Mehdi Keshavarz-Ghorabaee, Mohammad Amiri, Edmundas Kazimieras Zavadskas, Zenonas Turskis

**Citation:**
```
Keshavarz-Ghorabaee, M., Amiri, M., Zavadskas, E. K., & Turskis, Z. (2021). 
Determination of Objective Weights Using a New Method Based on the Removal Effects of Criteria (MEREC). 
Symmetry, 13(4), 525.
https://doi.org/10.3390/sym13040525
```

### VIKOR Method
**Original Developer:** Serafim Opricović

**Citations:**
```
Opricovic, S. (1998). Multicriteria Optimization of Civil Engineering Systems. 
Faculty of Civil Engineering, Belgrade.

Opricovic, S., & Tzeng, G. H. (2004). Compromise solution by MCDM methods: 
A comparative analysis of VIKOR and TOPSIS. 
European Journal of Operational Research, 156(2), 445-455.
https://doi.org/10.1016/S0377-2217(03)00020-1
```

### MAIRCA Method
**Original Developers:** Dragan Pamučar, Darko Božanić, Aleksandar Ranđelović

**Key Application Paper:**
```
Gigović, L., Pamučar, D., Bajić, Z., & Milićević, M. (2016). 
The combination of expert judgment and GIS-MAIRCA analysis for the selection of sites for ammunition depots. 
Sustainability, 8(4), 372.
https://doi.org/10.3390/su8040372
```

### CRITIC Method
**Original Developers:** Danae Diakoulaki, George Mavrotas, Lefteris Papayannakis

**Citation:**
```
Diakoulaki, D., Mavrotas, G., & Papayannakis, L. (1995). 
Determining objective weights in multiple criteria problems: The CRITIC method. 
Computers & Operations Research, 22(7), 763-770.
https://doi.org/10.1016/0305-0548(94)00059-H
```

### Entropy Method
**Foundational Work:** Claude Shannon (Information Theory)  
**MCDM Application:** Milan Zeleny

**Citations:**
```
Shannon, C. E. (1948). A mathematical theory of communication. 
Bell System Technical Journal, 27(3), 379-423.

Zeleny, M. (1982). Multiple Criteria Decision Making. 
McGraw-Hill, New York.
```

---

## Acknowledgments

We express our deep gratitude to all researchers who have contributed to the field of Multi-Criteria Decision Making. Their theoretical foundations and methodological innovations have made this tool possible.

**Special Thanks:**
- The original developers of each method for their groundbreaking research
- The academic community for continuous refinement and validation of these methods
- Researchers who publish detailed numerical examples that enable verification

---

## License

This tool is designed for academic and research purposes.

## Contributing

To add new methods or improve existing ones:
1. Implement the method in the appropriate `core/` module
2. Add tests in `tests/`
3. Document the formula in `FORMULAS.md`
4. Add verification examples

## Support

For questions or issues:
1. Check `FORMULAS.md` for implementation details
2. Review `verification/README.md` for verification guidance
3. Run with `--verbose` to debug calculations
4. Compare with known examples using `--compare`
