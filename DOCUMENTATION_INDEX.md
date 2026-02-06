# MCDM Calculator - Complete Documentation Index

## 📚 Documentation Overview

This project contains comprehensive documentation for researchers, students, and practitioners working with Multi-Criteria Decision Making methods.

---

## 🎯 Quick Navigation

### For First-Time Users
1. Start with **[README.md](README.md)** - Overview and quick start
2. Try the **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Common commands
3. Run an example from **[verification/examples/](mcdm_calculator/verification/examples/)**

### For Researchers
1. Read **[VERIFICATION_REPORT.md](VERIFICATION_REPORT.md)** - Proof of correctness
2. Check **[FORMULAS.md](mcdm_calculator/FORMULAS.md)** - Exact mathematical formulas
3. Review **[CITATIONS.md](CITATIONS.md)** - Academic references
4. Explore **[verification/README.md](mcdm_calculator/verification/README.md)** - Verification guide

### For Developers
1. Review **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - What was built
2. Check **[core/](mcdm_calculator/core/)** - Source code
3. Run **[test_quick.py](test_quick.py)** - Quick tests

---

## 📖 Documentation Files

### Main Documentation

| File | Purpose | Audience |
|------|---------|----------|
| **[README.md](README.md)** | Main project documentation, features, usage | Everyone |
| **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** | Common commands and quick tips | Users |
| **[FORMULAS.md](mcdm_calculator/FORMULAS.md)** | Exact mathematical formulas | Researchers |
| **[CITATIONS.md](CITATIONS.md)** | Complete academic citations | Researchers |

### Verification & Quality

| File | Purpose | Audience |
|------|---------|----------|
| **[VERIFICATION_REPORT.md](VERIFICATION_REPORT.md)** | Proof of implementation correctness | Researchers |
| **[verification/README.md](mcdm_calculator/verification/README.md)** | How to verify implementations | Researchers |
| **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** | What features were implemented | Developers |
| **[ATTRIBUTION_SUMMARY.md](ATTRIBUTION_SUMMARY.md)** | Citation additions summary | Researchers |

### Examples & Tutorials

| Location | Content | Purpose |
|----------|---------|---------|
| **[verification/examples/](mcdm_calculator/verification/examples/)** | Worked examples with data | Learning & Testing |
| **[verification/papers/](mcdm_calculator/verification/papers/)** | Examples from academic papers | Verification |

---

## 🔍 What Each Document Contains

### README.md
- **What:** Main project documentation
- **Contains:**
  - Feature overview
  - Installation instructions
  - Usage examples
  - Command-line options
  - Academic citations
- **Read this if:** You're new to the project

### FORMULAS.md
- **What:** Complete mathematical reference
- **Contains:**
  - Exact formulas for all methods
  - Step-by-step breakdowns
  - Implementation notes
  - Edge case handling
- **Read this if:** You need to understand the math or verify correctness

### CITATIONS.md
- **What:** Academic attribution document
- **Contains:**
  - Full citations for all methods
  - Author biographies
  - DOIs and publication details
  - How to cite this tool
- **Read this if:** You're writing a research paper

### VERIFICATION_REPORT.md
- **What:** Proof of implementation correctness
- **Contains:**
  - Comparison with published example
  - Step-by-step verification
  - Error analysis
  - Confidence assessment
- **Read this if:** You need to trust the implementation

### QUICK_REFERENCE.md
- **What:** Command cheat sheet
- **Contains:**
  - Common command patterns
  - Method combinations
  - File format examples
  - Troubleshooting tips
- **Read this if:** You just need to run the tool quickly

### verification/README.md
- **What:** Verification guide for researchers
- **Contains:**
  - How to verify implementations
  - How to add paper examples
  - Verification checklist
  - Common issues
- **Read this if:** You're validating against a paper

---

## 🎓 Learning Path

### Beginner Path
```
1. README.md (Overview)
   ↓
2. QUICK_REFERENCE.md (Commands)
   ↓
3. Run example1_phones.csv
   ↓
4. Try your own data
```

### Researcher Path
```
1. README.md (Overview)
   ↓
2. VERIFICATION_REPORT.md (Trust the tool)
   ↓
3. FORMULAS.md (Understand the math)
   ↓
4. CITATIONS.md (Cite properly)
   ↓
5. verification/README.md (Verify your results)
   ↓
6. Add your own paper examples
```

### Developer Path
```
1. README.md (Overview)
   ↓
2. IMPLEMENTATION_SUMMARY.md (What was built)
   ↓
3. core/ source code (How it works)
   ↓
4. test_quick.py (Test it)
   ↓
5. FORMULAS.md (Verify correctness)
```

---

## 📁 Project Structure

```
mcdm-research-tool/
├── README.md                          # Main documentation
├── QUICK_REFERENCE.md                 # Command reference
├── CITATIONS.md                       # Academic citations
├── FORMULAS.md → mcdm_calculator/     # Mathematical formulas
├── VERIFICATION_REPORT.md             # Proof of correctness
├── IMPLEMENTATION_SUMMARY.md          # Implementation details
├── ATTRIBUTION_SUMMARY.md             # Citation summary
│
├── mcdm_calculator/
│   ├── calculator.py                  # CLI tool
│   ├── FORMULAS.md                    # Mathematical reference
│   │
│   ├── core/                          # Implementation
│   │   ├── normalization.py
│   │   ├── weighting.py
│   │   └── ranking.py
│   │
│   ├── verification/                  # Examples & verification
│   │   ├── README.md                  # Verification guide
│   │   ├── examples/                  # Worked examples
│   │   │   ├── example1_phones.*
│   │   │   └── example2_projects.*
│   │   └── papers/                    # Academic examples
│   │       └── car_selection_topsis.*
│   │
│   └── tests/                         # Unit tests
│       └── test_verification.py
│
├── test_quick.py                      # Quick verification script
└── requirements.txt                   # Dependencies
```

---

## 🔗 Cross-References

### When reading about TOPSIS:
- **Formula:** See FORMULAS.md § 3.1
- **Citation:** See CITATIONS.md - TOPSIS section
- **Example:** See verification/papers/car_selection_topsis.csv
- **Verification:** See VERIFICATION_REPORT.md

### When reading about MEREC:
- **Formula:** See FORMULAS.md § 2.1
- **Citation:** See CITATIONS.md - MEREC section
- **Example:** See verification/examples/example1_phones.csv
- **Code:** See core/weighting.py - merec_weighting()

### When adding a new paper example:
1. See verification/README.md - "Adding New Verification Cases"
2. Follow format in verification/papers/car_selection_README.md
3. Use CITATIONS.md for proper attribution

---

## 📊 Documentation Statistics

- **Total Documentation Files:** 10+
- **Total Examples:** 3 (2 educational + 1 from paper)
- **Methods Documented:** 6 (TOPSIS, VIKOR, MAIRCA, MEREC, CRITIC, Entropy)
- **Academic Citations:** 6 primary + 2 foundational
- **Verification Status:** ✅ Verified against academic example

---

## 🆘 Getting Help

### I want to...

**...understand what this tool does**
→ Read [README.md](README.md)

**...run a quick calculation**
→ Check [QUICK_REFERENCE.md](QUICK_REFERENCE.md)

**...verify the implementation is correct**
→ Read [VERIFICATION_REPORT.md](VERIFICATION_REPORT.md)

**...understand the mathematical formulas**
→ Study [FORMULAS.md](mcdm_calculator/FORMULAS.md)

**...cite this tool in my paper**
→ See [CITATIONS.md](CITATIONS.md)

**...add my own paper example**
→ Follow [verification/README.md](mcdm_calculator/verification/README.md)

**...understand what was implemented**
→ Read [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)

**...see example commands**
→ Check [QUICK_REFERENCE.md](QUICK_REFERENCE.md)

---

## ✅ Documentation Completeness

- ✅ Installation guide
- ✅ Usage examples
- ✅ Mathematical formulas
- ✅ Academic citations
- ✅ Verification proof
- ✅ API reference (CLI)
- ✅ Worked examples
- ✅ Troubleshooting guide
- ✅ Contribution guidelines
- ✅ License information

---

**Last Updated:** February 2026

**Maintained by:** MCDM Calculator Project

**Documentation Status:** Complete and verified
