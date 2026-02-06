# MCDM Methods - Mathematical Formulas

This document describes the exact mathematical formulas implemented in this calculator.

---

## 1. Normalization Methods

### 1.1 Vector Normalization
Used primarily in **TOPSIS**.

**Formula:**
```
n_ij = x_ij / sqrt(sum(x_ij^2)) for all i
```

Where:
- `x_ij` = original value for alternative i, criterion j
- `n_ij` = normalized value

**Properties:**
- Results in unit vector for each criterion
- Range: depends on data distribution

---

### 1.2 Min-Max Normalization

**For Benefit Criteria (higher is better):**
```
n_ij = (x_ij - min(x_j)) / (max(x_j) - min(x_j))
```

**For Cost Criteria (lower is better):**
```
n_ij = (max(x_j) - x_ij) / (max(x_j) - min(x_j))
```

**Properties:**
- Range: [0, 1]
- Best alternative = 1, Worst = 0

---

### 1.3 Linear Normalization (Max/Min)
Used in **MAIRCA**.

**For Benefit Criteria:**
```
n_ij = x_ij / max(x_j)
```

**For Cost Criteria:**
```
n_ij = min(x_j) / x_ij
```

**Properties:**
- Range: (0, 1]
- Best alternative = 1

---

### 1.4 Sum Normalization
Used in **Entropy** method.

**Formula:**
```
n_ij = x_ij / sum(x_j) for all i
```

**Properties:**
- Each column sums to 1
- Represents proportional contribution

---

## 2. Weighting Methods

### 2.1 MEREC (Method based on Removal Effects of Criteria)

**Reference:** Keshavarz-Ghorabaee et al. (2021)

**Step 1: Normalization**

For Benefit criteria:
```
n_ij = min(x_j) / x_ij
```

For Cost criteria:
```
n_ij = x_ij / max(x_j)
```

**Step 2: Overall Performance**
```
S_i = ln(1 + (1/m) * sum(|ln(n_ij)|)) for all j
```

Where m = number of criteria

**Step 3: Performance without criterion j**
```
S'_ij = ln(1 + (1/m) * sum(|ln(n_ik)|)) for all k ≠ j
```

**Step 4: Removal Effect**
```
E_j = sum(|S'_ij - S_i|) for all i
```

**Step 5: Final Weights**
```
w_j = E_j / sum(E_j)
```

**Properties:**
- Objective weighting based on information removal
- Higher E_j = more important criterion

---

### 2.2 Entropy Method

**Reference:** Shannon (1948), Zeleny (1982)

**Step 1: Normalize (Sum normalization)**
```
p_ij = x_ij / sum(x_i) for all i
```

**Step 2: Calculate Entropy**
```
e_j = -(1/ln(m)) * sum(p_ij * ln(p_ij)) for all i
```

Where m = number of alternatives

**Step 3: Degree of Diversification**
```
d_j = 1 - e_j
```

**Step 4: Final Weights**
```
w_j = d_j / sum(d_j)
```

**Properties:**
- Lower entropy = higher weight (more discriminating)
- Range: e_j ∈ [0, 1]

---

### 2.3 CRITIC (Criteria Importance Through Intercriteria Correlation)

**Reference:** Diakoulaki et al. (1995)

**Step 1: Normalize (Min-Max)**
```
n_ij = (x_ij - min(x_j)) / (max(x_j) - min(x_j))
```

**Step 2: Standard Deviation**
```
σ_j = std(n_j)
```

**Step 3: Correlation Matrix**
```
R = correlation_matrix(normalized_matrix)
```

**Step 4: Conflict Measure**
```
C_j = sum(1 - r_jk) for all k
```

Where r_jk is correlation between criteria j and k

**Step 5: Information Content**
```
I_j = σ_j * C_j
```

**Step 6: Final Weights**
```
w_j = I_j / sum(I_j)
```

**Properties:**
- Considers both variability and correlation
- Higher conflict + higher std = higher weight

---

## 3. Ranking Methods

### 3.1 TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution)

**Reference:** Hwang & Yoon (1981)

**Step 1: Vector Normalization**
```
n_ij = x_ij / sqrt(sum(x_ij^2))
```

**Step 2: Weighted Normalized Matrix**
```
v_ij = w_j * n_ij
```

**Step 3: Ideal Solutions**

For Benefit criteria:
```
A*_j = max(v_ij)  (Ideal)
A-_j = min(v_ij)  (Anti-ideal)
```

For Cost criteria:
```
A*_j = min(v_ij)  (Ideal)
A-_j = max(v_ij)  (Anti-ideal)
```

**Step 4: Separation Measures (Euclidean Distance)**
```
S*_i = sqrt(sum((v_ij - A*_j)^2))  (Distance to ideal)
S-_i = sqrt(sum((v_ij - A-_j)^2))  (Distance to anti-ideal)
```

**Step 5: Closeness Coefficient**
```
C_i = S-_i / (S*_i + S-_i)
```

**Ranking:** Sort by C_i descending (higher is better)

**Properties:**
- Range: C_i ∈ [0, 1]
- C_i = 1: Best alternative
- C_i = 0: Worst alternative

---

### 3.2 VIKOR (VIseKriterijumska Optimizacija I Kompromisno Resenje)

**Reference:** Opricovic & Tzeng (2004)

**Step 1: Best and Worst Values**

For Benefit criteria:
```
f*_j = max(x_ij)  (Best)
f-_j = min(x_ij)  (Worst)
```

For Cost criteria:
```
f*_j = min(x_ij)  (Best)
f-_j = max(x_ij)  (Worst)
```

**Step 2: Utility and Regret Measures**
```
S_i = sum(w_j * (f*_j - x_ij) / (f*_j - f-_j))  (Group utility)
R_i = max(w_j * (f*_j - x_ij) / (f*_j - f-_j))  (Individual regret)
```

**Step 3: VIKOR Index**
```
Q_i = v * (S_i - S*) / (S- - S*) + (1-v) * (R_i - R*) / (R- - R*)
```

Where:
- S* = min(S_i), S- = max(S_i)
- R* = min(R_i), R- = max(R_i)
- v = 0.5 (default, weight for strategy of maximum group utility)

**Ranking:** Sort by Q_i ascending (lower is better)

**Properties:**
- Q_i ∈ [0, 1]
- Compromise solution between group utility and individual regret

---

### 3.3 MAIRCA (Multi-Attributive Border Approximation area Comparison)

**Reference:** Gigović et al. (2016)

**Step 1: Theoretical Rating Matrix**
```
T_pij = (1/m) * w_j
```

Where m = number of alternatives

**Step 2: Real Rating Matrix (Linear Normalization)**

For Benefit:
```
n_ij = x_ij / max(x_j)
```

For Cost:
```
n_ij = min(x_j) / x_ij
```

Then:
```
T_rij = T_pij * n_ij
```

**Step 3: Gap Matrix**
```
G_ij = T_pij - T_rij
```

**Step 4: Total Gap**
```
Q_i = sum(G_ij) for all j
```

**Ranking:** Sort by Q_i ascending (lower gap is better)

**Properties:**
- Gap represents distance from theoretical ideal
- Q_i ≥ 0
- Lower gap = better alternative

---

## Implementation Notes

### Handling Edge Cases

1. **Division by Zero:**
   - Add small epsilon (1e-9) to denominators
   - Replace zero ranges with 1

2. **Logarithm of Zero:**
   - Replace 0 with small epsilon (1e-9) before ln()

3. **Identical Values:**
   - If all values in a criterion are identical, assign equal normalized values

### Numerical Precision

- All calculations use `float64` (NumPy default)
- Weights are normalized to sum exactly to 1.0
- Rounding for display: typically 4-6 decimal places

---

## References & Citations

For complete citations and author information, see **CITATIONS.md** in the project root.

### Quick References

1. **TOPSIS:**  
   Hwang, C. L., & Yoon, K. (1981). Multiple Attribute Decision Making: Methods and Applications. Springer-Verlag, New York.

2. **VIKOR:**  
   Opricovic, S., & Tzeng, G. H. (2004). Compromise solution by MCDM methods: A comparative analysis of VIKOR and TOPSIS. European Journal of Operational Research, 156(2), 445-455.

3. **CRITIC:**  
   Diakoulaki, D., Mavrotas, G., & Papayannakis, L. (1995). Determining objective weights in multiple criteria problems: The CRITIC method. Computers & Operations Research, 22(7), 763-770.

4. **MEREC:**  
   Keshavarz-Ghorabaee, M., Amiri, M., Zavadskas, E. K., & Turskis, Z. (2021). Determination of Objective Weights Using a New Method Based on the Removal Effects of Criteria (MEREC). Symmetry, 13(4), 525.

5. **MAIRCA:**  
   Gigović, L., Pamučar, D., Bajić, Z., & Milićević, M. (2016). The combination of expert judgment and GIS-MAIRCA analysis for the selection of sites for ammunition depots. Sustainability, 8(4), 372.

6. **Entropy:**  
   Shannon, C. E. (1948). A mathematical theory of communication. Bell System Technical Journal, 27(3), 379-423.  
   Zeleny, M. (1982). Multiple Criteria Decision Making. McGraw-Hill, New York.

---

**Note:** This implementation faithfully follows the formulas from the original papers. Any deviations or optimizations are documented in the code comments.

