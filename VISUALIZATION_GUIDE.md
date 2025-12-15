# How to Generate and View the Performance Graphs

## Quick Start

### 1. Install Required Packages

```bash
# Make sure you're in your virtual environment
source mSMD_env/bin/activate  # On Windows: mSMD_env\Scripts\activate

# Install visualization packages
pip install matplotlib seaborn numpy pandas
```

### 2. Run the Visualization Script

```bash
python visualize_results.py
```

### 3. View Generated Graphs

All graphs will be saved in: `results/graphs/`

The script will generate:
- ✅ `figure2_performance_different_os.png`
- ✅ `figure3_performance_same_os.png`
- ✅ `figure4_shared_pages_proportion.png`
- ✅ `figure5_response_time_comparison.png`
- ✅ `figure6_average_runtime.png`
- ✅ `figure7_pages_sharing_comparison.png`
- ✅ `figure8_comparison_reduction.png`
- ✅ `summary_dashboard.png`
- ✅ `RESULTS_SUMMARY.txt`

---

## What Each Graph Shows

### Figure 2: Performance with Different Guest OS
**Shows:** Normalized system performance (1.0 = baseline)
**Finding:** 8-VMs-8G achieves 1.18x performance improvement
**Use in Report:** Section 5.1 - Performance Metrics

### Figure 3: Performance with Same OS
**Shows:** Higher performance when VMs run identical OS
**Finding:** Up to 1.20x improvement (better than Fig 2)
**Use in Report:** Section 6.1 - Comparison with Paper

### Figure 4: Shared Pages Proportion
**Shows:** More VMs = more page sharing opportunities
**Finding:** 8 VMs show lowest "shared times" metric
**Use in Report:** Section 5.1 - Memory Efficiency

### Figure 5: Response Time Comparison
**Shows:** mSMD vs KSM response times
**Finding:** mSMD is 30-40% faster than KSM
**Use in Report:** Section 5.2 - Response Time Analysis

### Figure 6: Average Runtime
**Shows:** VM execution time (mSMD vs KSM)
**Finding:** mSMD has consistently shorter runtime
**Use in Report:** Section 5.2 - Response Time Analysis

### Figure 7: Pages Sharing (4 Workloads)
**Shows:** Page sharing over time for each workload
**Finding:** mSMD detects 25-30% more shared pages
**Use in Report:** Section 4.2 - Workload Specifications

### Figure 8: Comparison Reduction
**Shows:** Reduction in unnecessary page comparisons
**Finding:** 24.5-27.5% reduction across workloads
**Use in Report:** Section 5.4 - Comparison Reduction

### Summary Dashboard
**Shows:** All key metrics in one view
**Finding:** Complete performance overview
**Use in Report:** Executive Summary or Conclusion

---

## Customizing with Your Actual Results

### Option 1: Manual Update

Open `visualize_results.py` and modify the data arrays:

```python
# Example: Update Figure 2 with your actual results
def generate_figure2_performance_different_os():
    configurations = ['1-VM-4G', '2-VM-4G', '4-VM-4G', '8-VM-4G',
                     '1-VM-8G', '2-VM-8G', '4-VM-8G', '8-VM-8G']
    
    # Replace these with YOUR actual measurements
    performance = [1.02, 1.05, 1.10, 1.15, 1.03, 1.07, 1.12, 1.18]
    #              ^^^^ Update these values ^^^^
```

### Option 2: Load from JSON Results

If you have results in JSON format:

```python
import json

# Load your actual results
with open('results/your_results.json') as f:
    data = json.load(f)

performance = data['performance_metrics']
```

### Option 3: Use CSV Data

```python
import pandas as pd

# Load from CSV
df = pd.read_csv('results/metrics.csv')
performance = df['normalized_performance'].tolist()
```

---

## Including Graphs in Your Report

### Method 1: Markdown (Recommended)

In your `IMPLEMENTATION_REPORT_TEMPLATE.md`:

```markdown
### Figure 1: Memory Reduction Comparison

![Memory Reduction](results/graphs/figure2_performance_different_os.png)

**Analysis:** The graph shows that mSMD achieves a normalized performance 
of 1.18 in the 8-VMs-8G configuration, representing an 18% improvement 
over the baseline...
```

### Method 2: Copy Images

1. Navigate to `results/graphs/`
2. Copy PNG files
3. Paste into your Word document or PDF

### Method 3: Reference by Path

```
See Figure 2 (results/graphs/figure2_performance_different_os.png) for 
performance comparison across different configurations.
```

---

## Understanding the Data

### Sample Data vs Real Data

**Current Status:** The graphs use **sample/expected data** based on the paper's findings.

**Your Task:** Replace with **actual experimental results** when you run the implementation.

### Expected vs Actual Comparison

| Metric | Expected (Paper) | Your Result | Variance |
|--------|------------------|-------------|----------|
| Memory Reduction | 20-28% | ___ % | ___ % |
| Comparison Reduction | 24.5-27.5% | ___ % | ___ % |
| Response Time | Significant | ___ ms | ___ % |
| CPU Overhead | <1% | ___ % | ___ % |

---

## Troubleshooting

### "Module not found: matplotlib"
```bash
pip install matplotlib seaborn numpy pandas
```

### "Permission denied" when saving
```bash
# Create directory manually
mkdir -p results/graphs
```

### "Figure not showing"
```bash
# The script saves to file automatically
# Check results/graphs/ folder for PNG files
```

### Graphs look different from paper
This is expected! The sample data is approximate. Your actual experimental 
results will differ based on:
- Hardware configuration
- VM workloads
- System load
- Implementation details

---

## Quick Commands Reference

```bash
# Install dependencies
pip install -r requirements.txt

# Generate all graphs
python visualize_results.py

# View results
cd results/graphs
ls -la

# Open a specific graph (Windows)
start figure2_performance_different_os.png

# Open a specific graph (Linux)
xdg-open figure2_performance_different_os.png

# Open summary
cat RESULTS_SUMMARY.txt
```

---

## Next Steps

1. ✅ **Run the script** to generate sample graphs
2. ✅ **Review the graphs** to understand expected results
3. ✅ **Run your experiments** with actual workloads
4. ✅ **Collect real data** from your implementation
5. ✅ **Update the script** with your actual measurements
6. ✅ **Regenerate graphs** with real data
7. ✅ **Include in report** with analysis

---

## Tips for Your Report

### Good Practice ✓
- Include all 8 figures
- Explain what each graph shows
- Compare with paper's findings
- Discuss any deviations
- Use high-resolution images (300 DPI)

### Avoid ✗
- Just pasting graphs without explanation
- Using low-quality screenshots
- Not comparing with paper's results
- Ignoring differences in findings

---

**Your graphs are ready! Run the script and check `results/graphs/` folder.** 📊

