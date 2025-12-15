# mSMD Implementation Report Template

**Student Name:** [Your Name]  
**Registration Number:** [Your Reg No]  
**Program:** Software Engineering  
**Date:** [Date]  
**Paper:** "Optimization of Virtual Machines Performance Using Fuzzy Hashing and Genetic Algorithm-Based Memory Deduplication of Static Pages"  
**Authors:** N. Jagadeeswari, V. Mohanraj, Y. Suresh, J. Senthilkumar  
**Published:** Automatika, 2023, 64(4), 868-877

---

## 1. EXECUTIVE SUMMARY

### 1.1 Objectives
This implementation report documents the reproduction and implementation of the mSMD (modified Static Memory Deduplication) approach from the selected research paper. The goal is to:
- Understand the four core algorithms (Fuzzy Hashing, GA, MSPT, Deduplication)
- Implement each component based on the paper's methodology
- Set up a simulation environment with KVM hypervisor
- Reproduce the experimental results with four workloads
- Validate the findings against the original paper

### 1.2 Key Findings
[To be completed after implementation]
- Memory reduction achieved: ____%
- Response time improvement: ____%
- CPU overhead: ____%
- Comparison reduction: ____%

---

## 2. IMPLEMENTATION ENVIRONMENT

### 2.1 Hardware Specifications
| Component | Specification |
|-----------|---------------|
| CPU | [e.g., Intel Core i5, 8th Gen] |
| RAM | [Total GB] |
| Storage | [Total GB] |
| OS | [Linux distribution] |

### 2.2 Software Stack
| Software | Version | Purpose |
|----------|---------|---------|
| KVM | [version] | Hypervisor |
| QEMU | [version] | Emulator |
| Linux Kernel | [version] | Host OS |
| Ubuntu | 16.04 | Guest OS |
| Python | 3.8+ | Implementation language |
| ssdeep | [version] | Fuzzy hashing |
| perf | [version] | Performance monitoring |

### 2.3 Development Tools
- **IDE:** [VS Code / PyCharm / Other]
- **Version Control:** Git
- **Monitoring:** Linux perf, /proc/meminfo
- **Documentation:** Markdown, PNG for screenshots

---

## 3. IMPLEMENTATION METHODOLOGY

### 3.1 Module 1: Fuzzy Hashing & Application Clustering

#### Description
Application clustering using fuzzy hashing to identify similar applications, followed by Hierarchical Agglomerative Clustering (HAC) to group them.

#### Implementation Details

**Algorithm 1: Formation of Application Clusters**

```
FUZZY_HASH_MODULE:
  - Function: compute_fuzzy_hash(data)
    * Implements rolling hash + MD5 combination
    * Input: application binary content
    * Output: fuzzy hash fingerprint (16 chars)
  
  - Function: calculate_similarity(hash1, hash2)
    * Uses normalized edit distance
    * Returns similarity score 0-100
    * Threshold: 30%
  
  - Function: cluster_applications(applications)
    * HAC implementation
    * Similarity-based clustering
    * Returns clustered application groups
```

**Code Location:** `msmd_implementation.py` - Lines [___-___]

**Key Parameters:**
- Similarity Threshold: 30%
- Clustering Method: Hierarchical Agglomerative
- Distance Metric: Edit distance / Hamming distance

#### Experimental Results
[To be filled after running]

**Test Case 1: Two Identical Applications**
- Input: 2 applications with identical content
- Expected: Similarity = 100%, Cluster size = 2
- Actual: ____
- Status: ✓ PASS / ✗ FAIL

**Test Case 2: Three Applications (Mixed)**
- Input: 3 apps (App1 and App2 similar, App3 different)
- Expected: 2 clusters
- Actual: ____
- Status: ✓ PASS / ✗ FAIL

**Execution Time:** _____ ms

---

### 3.2 Module 2: Genetic Algorithm for Page Similarity Detection

#### Description
Detects similar memory pages within clustered applications using genetic algorithm with fitness evaluation based on object dump comparison.

#### Implementation Details

**Algorithm 2: Identification of Static Similar Pages**

```
GENETIC_ALGORITHM_MODULE:
  - Parameters:
    * Population size: 50
    * Generations: 20
    * Mutation rate: 10%
    * Fitness threshold: 70%
  
  - Function: fitness_function(page1, page2)
    * Input: Two 4KB pages
    * Compares object dumps
    * Returns similarity 0-100
    * Identical dumps = 100 fitness
  
  - Function: detect_similar_pages(pages)
    * Initial population: All page pairs
    * Selection: Roulette wheel
    * Mutation: Random page swapping
    * Convergence: 20 generations
```

**Code Location:** `msmd_implementation.py` - Lines [___-___]

**Key Parameters:**
- Page Size: 4096 bytes (4KB)
- Population Size: 50 pairs
- Generations: 20
- Mutation Rate: 10%
- Similarity Threshold: 70%

#### Experimental Results
[To be filled after running]

**Test Case 1: Two Identical Pages**
- Input: 2 pages with identical content
- Expected Fitness: 100%
- Actual: ____
- Pages Detected as Similar: ✓ YES / ✗ NO

**Test Case 2: GA Convergence**
- Input: 10 pages (5 pairs of similar)
- Generations: 20
- Expected Similar Pairs Found: ≥5
- Actual: ____

**Execution Time:** _____ ms

---

### 3.3 Module 3: Multilevel Shared Page Table

#### Description
Creates and maintains a multilevel data structure to store pre-computed page similarity relationships for efficient online lookup.

#### Implementation Details

**Algorithm 3: Multilevel Shared Page Table**

```
MULTILEVEL_SHARED_PAGE_TABLE:
  - Data Structure: Hash-based index
    * Key: page_id
    * Value: SharedPageTableEntry
  
  - Entry Structure:
    * entry_id: unique identifier
    * primary_page_id: first page in group
    * similar_pages: list of related pages
    * content_signature: hash of content
    * cluster_id: application cluster
  
  - Function: build_table(pages, similar_pairs)
    * Creates entries from similarity relationships
    * Maps all pages to entries
    * Returns table size
  
  - Function: lookup(page_id)
    * O(1) lookup time
    * Returns entry or None
```

**Code Location:** `msmd_implementation.py` - Lines [___-___]

#### Experimental Results
[To be filled after running]

**Test Case 1: Table Creation**
- Input: 20 pages, 8 similar pairs
- Expected Entries: 8
- Actual: ____
- Memory Used: _____ KB

**Test Case 2: Lookup Performance**
- Input: 1000 random page lookups
- Average Lookup Time: _____ μs
- Cache Hit Rate: _____%

---

### 3.4 Module 4: Memory Deduplication

#### Description
Performs actual memory page merging using the pre-computed multilevel shared page table during the online phase when VMs are running.

#### Implementation Details

**Algorithm 4: Memory Deduplication Implementation**

```
MEMORY_DEDUPLICATION_ENGINE:
  - Function: merge_pages(vm_pages)
    * Input: Pages from running VMs
    * For each page:
      - Check if in MSPT
      - If found: merge with shared pages
      - Apply copy-on-write protection
    * Output: merge count, memory saved
  
  - Copy-on-Write Mechanism:
    * Shared pages marked read-only
    * On write: trigger page fault
    * Create new page copy
    * Update page table entry
```

**Code Location:** `msmd_implementation.py` - Lines [___-___]

#### Experimental Results
[To be filled after running]

**Test Case 1: Basic Deduplication**
- Input: 2 VMs with 10 shared pages each
- Pages Before Merge: 20
- Expected Merged: ≥10
- Actual Merged: ____
- Memory Saved: _____ MB

**Test Case 2: Multi-VM Scenario**
- Input: 4 VMs with mixed shared pages
- Total Pages: 100
- Expected Dedup Rate: 25-30%
- Actual: ____
- Memory Saved: _____ MB

---

## 4. EXPERIMENTAL SETUP & WORKLOADS

### 4.1 Simulation Environment

#### VM Configuration
```
Number of VMs: [1, 2, 4, 8]
Memory per VM: [4GB, 8GB]
vCPUs per VM: 2
Guest OS: Ubuntu 16.04 LTS
```

#### Host Configuration
```
Hypervisor: KVM + QEMU
CPU allocation: [As available]
RAM allocation: 32GB+
```

### 4.2 Workload Specifications

#### Workload 1: .NET Application

**Configuration:**
```
Application: .NET Web Application
Command: [command to run]
Duration: [minutes]
Concurrent Requests: [number]
```

**Expected Results:**
- Page sharing rate: _____%
- Memory usage: _____ MB
- Response time: _____ ms

**Actual Results:**
[To be filled]

**Evidence:** [Screenshot/log file name: _______________]

---

#### Workload 2: Apache HTTP Server

**Configuration:**
```
Server: Apache HTTPd
Tool: Apache Bench (ab)
Concurrent Requests: 24
Duration: [minutes]
Requests/sec: [target]
```

**Expected Results:**
- Pages shared: _____
- Response time improvement: _____%
- Throughput: _____ req/sec

**Actual Results:**
[To be filled]

**Evidence:** [Screenshot/log file name: _______________]

---

#### Workload 3: MySQL Database

**Configuration:**
```
Database: MySQL 5.7
Benchmark: SysBench
Threads: [number]
Duration: [minutes]
Workload: OLTP-like
```

**Expected Results:**
- TPS (Transactions/sec): _____
- Memory dedup rate: _____%
- Latency improvement: _____%

**Actual Results:**
[To be filled]

**Evidence:** [Screenshot/log file name: _______________]

---

#### Workload 4: Genymotion (Android Emulator)

**Configuration:**
```
Emulator: Genymotion
Android Version: [version]
AVD Instance: [count]
Duration: [minutes]
Apps Running: [list]
```

**Expected Results:**
- Memory usage: _____ MB
- Page sharing: _____%
- Performance impact: _____%

**Actual Results:**
[To be filled]

**Evidence:** [Screenshot/log file name: _______________]

---

## 5. PERFORMANCE METRICS & RESULTS

### 5.1 Memory Efficiency

#### Table 1: Memory Reduction Results

| Configuration | Total Pages | Pages Merged | Memory Saved | Reduction % |
|---------------|-------------|-------------|-------------|------------|
| 1-VM-4G | ___ | ___ | ___ MB | ___% |
| 2-VM-4G | ___ | ___ | ___ MB | ___% |
| 4-VM-4G | ___ | ___ | ___ MB | ___% |
| 8-VM-4G | ___ | ___ | ___ MB | ___% |
| 1-VM-8G | ___ | ___ | ___ MB | ___% |
| 2-VM-8G | ___ | ___ | ___ MB | ___% |
| 4-VM-8G | ___ | ___ | ___ MB | ___% |
| 8-VM-8G | ___ | ___ | ___ MB | ___% |

#### Figure 1: Memory Reduction Comparison

[Insert graph comparing mSMD vs KSM]

```
[Your execution will generate actual data]
Expected range: 20-28% reduction
```

---

### 5.2 Response Time Analysis

#### Table 2: Response Time (ms)

| Configuration | KSM (baseline) | mSMD | Improvement |
|---|---|---|---|
| 1-VM-4G | ___ | ___ | ___% |
| 2-VM-4G | ___ | ___ | ___% |
| 4-VM-4G | ___ | ___ | ___% |
| 8-VM-4G | ___ | ___ | ___% |
| 1-VM-8G | ___ | ___ | ___% |
| 2-VM-8G | ___ | ___ | ___% |
| 4-VM-8G | ___ | ___ | ___% |
| 8-VM-8G | ___ | ___ | ___% |

#### Figure 2: Response Time Comparison

[Insert graph showing mSMD < KSM]

---

### 5.3 CPU Overhead

#### Table 3: CPU Overhead Analysis

| Phase | Operation | CPU Usage | Overhead |
|---|---|---|---|
| Offline | Fuzzy Hashing | ___% | Acceptable |
| Offline | Genetic Algorithm | ___% | Acceptable |
| Offline | MSPT Building | ___% | Acceptable |
| Online | Page Merging | ___% | <1% (expected) |
| Online | Copy-on-Write | ___% | Minimal |

---

### 5.4 Unnecessary Comparison Reduction

#### Table 4: Comparison Reduction by Workload

| Workload | Comparisons (KSM) | Comparisons (mSMD) | Reduction % |
|---|---|---|---|
| .NET Application | ___ | ___ | ___% |
| Apache HTTP Server | ___ | ___ | ___% |
| MySQL Database | ___ | ___ | ___% |
| Genymotion | ___ | ___ | ___% |
| **Average** | | | **___% (expected: 24-27%)** |

#### Figure 3: Unnecessary Comparison Reduction

[Insert bar chart showing reduction percentages]

---

## 6. COMPARISON WITH PAPER'S FINDINGS

### 6.1 Expected vs. Actual Results

#### Memory Reduction
- **Paper's Result:** 28% reduction in unnecessary comparisons
- **Our Result:** _____%
- **Variance:** ±_____%
- **Analysis:** [Explain differences if any]

#### Response Time
- **Paper's Finding:** Significantly lower than KSM
- **Our Finding:** [Actual measurements]
- **Consistency:** ✓ CONSISTENT / ✗ DIFFERENT

#### CPU Overhead
- **Paper's Claim:** <1% CPU overhead per VM
- **Our Measurement:** _____%
- **Status:** ✓ ACHIEVED / ✗ EXCEEDED

#### Page Sharing Efficiency
- **Paper's Result:** 25-30% higher than KSM
- **Our Result:** _____%
- **Status:** ✓ REPLICATED / ✗ DEVIATION

---

### 6.2 Deviation Analysis

[If results differ from paper, explain why]

#### Potential Reasons:
1. Hardware differences
2. VM configuration variations
3. Workload implementation differences
4. Algorithm parameter tuning
5. Environmental factors

**Detailed Analysis:**
[Your analysis here]

---

## 7. CHALLENGES ENCOUNTERED & SOLUTIONS

### Challenge 1: [Description]
**Issue:** [What was the problem]  
**Root Cause:** [Why it happened]  
**Solution:** [How it was solved]  
**Resolution Status:** ✓ RESOLVED / ✗ PARTIALLY RESOLVED / ✗ UNRESOLVED

---

### Challenge 2: [Description]
**Issue:** [What was the problem]  
**Root Cause:** [Why it happened]  
**Solution:** [How it was solved]  
**Resolution Status:** ✓ RESOLVED / ✗ PARTIALLY RESOLVED / ✗ UNRESOLVED

---

[Add more challenges as encountered]

---

## 8. IMPLEMENTATION INSIGHTS & OBSERVATIONS

### 8.1 Strengths of mSMD Approach
1. **Offline Processing Benefits:** Eliminates online overhead, faster response times
2. **Clustering Efficiency:** Reduces unnecessary comparisons by ~27%
3. **Hardware Independence:** No specific hardware requirements beyond standard Linux
4. **Scalability:** Works well with increasing number of VMs

### 8.2 Limitations Found
1. **Code Segment Only:** Limited to code section, doesn't handle data/stack segments
2. **[Other limitation]:** [Description]

### 8.3 Practical Recommendations
1. **For Production Deployment:**
   - Implement hardware-accelerated hashing for large applications
   - Add dynamic threshold adjustment based on workload
   - Implement distributed MSPT for multi-node clusters

2. **For Future Research:**
   - Extend to data and stack segments
   - Integrate with live VM migration
   - Add machine learning for optimal parameter tuning

---

## 9. SUPPORTING EVIDENCE

### 9.1 Screenshots

#### Screenshot 1: KVM Environment Setup
[Insert screenshot]
- Shows: [What is visible]
- Date/Time: [When captured]
- Description: [Brief description]

#### Screenshot 2: mSMD Execution - Fuzzy Hashing Phase
[Insert screenshot]
- Shows: Fuzzy hashing output
- Duration: [Time taken]
- Status: [Result]

#### Screenshot 3: mSMD Execution - GA Phase
[Insert screenshot]
- Shows: GA convergence, similar pages found
- Duration: [Time taken]
- Status: [Result]

#### Screenshot 4: mSMD Execution - Online Deduplication
[Insert screenshot]
- Shows: Memory merging, pages reduced
- Memory Saved: [Amount]
- Status: [Result]

#### Screenshot 5: Performance Monitoring
[Insert screenshot]
- Shows: perf output, memory stats, CPU usage
- Duration: [Monitoring period]
- Configuration: [VM setup]

---

### 9.2 Log Files

#### Log File 1: Module Execution Log
```
File: msmd_execution.log
Size: _____ KB
Contains:
  - Fuzzy hashing results
  - Clustering decisions
  - GA iterations
  - Pages identified
  - Merge operations
```

[Excerpt of log file]

---

#### Log File 2: Performance Metrics Log
```
File: performance_metrics.log
Contains:
  - Memory before/after
  - Response times
  - CPU usage
  - Page fault counts
  - Cache hit rates
```

[Excerpt of log file]

---

### 9.3 Execution Outputs

#### Output File 1: Application Clustering Results
```json
{
  "total_applications": 8,
  "clusters_formed": 3,
  "cluster_composition": {
    "cluster_1": [1, 2, 3],
    "cluster_2": [4, 5],
    "cluster_3": [6, 7, 8]
  },
  "avg_similarity": "___"
}
```

---

#### Output File 2: Page Similarity Detection Results
```json
{
  "total_pages_analyzed": 320,
  "similar_pairs_found": __,
  "similarity_threshold": "70%",
  "avg_fitness_score": "___%"
}
```

---

## 10. CONCLUSION

### 10.1 Summary of Implementation

This implementation successfully reproduced the mSMD approach from the research paper. We:

1. ✓ Implemented all four core modules (Fuzzy Hashing, GA, MSPT, Deduplication)
2. ✓ Set up a KVM-based virtualization environment
3. ✓ Ran comprehensive experiments with 4 workloads
4. ✓ Collected performance metrics and compared with paper's findings
5. ✓ Achieved memory reduction of ____% (expected: 20-28%)
6. ✓ Demonstrated response time improvement of ____% over KSM

### 10.2 Key Achievements

- **Functionality:** All algorithms implemented and working as specified
- **Performance:** Results align with paper's findings (±____%)
- **Robustness:** Tested with multiple VM configurations and workloads
- **Documentation:** Complete implementation with comments and examples

### 10.3 Validation Results

| Aspect | Status | Evidence |
|--------|--------|----------|
| Fuzzy Hashing | ✓ WORKING | [Test results] |
| Application Clustering | ✓ WORKING | [Test results] |
| Genetic Algorithm | ✓ WORKING | [Test results] |
| Page Similarity Detection | ✓ WORKING | [Test results] |
| MSPT Construction | ✓ WORKING | [Test results] |
| Memory Deduplication | ✓ WORKING | [Test results] |
| Performance Metrics | ✓ VALIDATED | [Test results] |

### 10.4 Overall Assessment

**Implementation Status:** ✓ COMPLETE

**Code Quality:** [Excellent / Good / Satisfactory]

**Test Coverage:** [100% / 90% / 80%] of algorithms

**Documentation:** [Complete / Comprehensive / Adequate]

---

## 11. FUTURE IMPROVEMENTS

### Recommended Enhancements

1. **Performance Optimization:**
   - Implement parallelized fuzzy hashing using GPU
   - Add caching mechanisms for MSPT lookups
   - Optimize GA convergence with adaptive parameters

2. **Feature Expansion:**
   - Extend to data and stack segments
   - Add live migration support
   - Implement distributed MSPT for cloud environments

3. **Research Opportunities:**
   - Machine learning-based parameter tuning
   - Security-aware deduplication
   - Cross-VM interference analysis

---

## 12. REFERENCES

### Paper Reference
[1] Jagadeeswari, N., Mohanraj, V., Suresh, Y., & Senthilkumar, J. (2023). Optimization of virtual machines performance using fuzzy hashing and genetic algorithm-based memory deduplication of static pages. *Automatika*, 64(4), 868-877.

### Related Works Referenced in Comparative Analysis
[2] Zhong, Y., Berger, D.S., et al. (2024). Managing Memory Tiers with CXL in Virtualized Environments. *USENIX OSDI '24*.

[3] Jia, W., Zhang, J., Shan, J., & Ding, X. (2024). Effective Huge Page Strategies for TLB Miss Reduction in Nested Virtualization. *IEEE Transactions on Computers*, 27(9).

[4] Jalalian, S., Patel, S., et al. (2024). EXTMEM: Enabling Application-Aware Virtual Memory Management. *USENIX ATC '24*.

[5] Shaikh, G.E., & Shrawankar, U. (2015). Dynamic Memory Allocation Technique for Virtual Machines. *IEEE Conference*.

### Technical References
- KVM Documentation: https://www.linux-kvm.org/
- Linux Perf: https://perf.wiki.kernel.org/
- Fuzzy Hashing (ssdeep): https://ssdeep-project.github.io/

---

## APPENDICES

### Appendix A: Source Code Listings

[Include main Python implementation files]

### Appendix B: Raw Performance Data

[Include detailed performance metrics in tabular format]

### Appendix C: VM Configuration Files

[Include sample KVM/QEMU configuration files]

### Appendix D: Workload Scripts

[Include scripts used for running workloads]

---

**Report Completed:** [Date]  
**Student Signature:** ___________________  
**Instructor Review:** [Space for feedback]

