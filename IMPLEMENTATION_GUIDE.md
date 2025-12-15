# mSMD Implementation Guide
## Memory Deduplication of Static Pages using Fuzzy Hashing and Genetic Algorithm

### Project Overview
This document guides the implementation of the mSMD (modified Static Memory Deduplication) approach from the paper:
- **Title**: "Optimization of Virtual Machines Performance Using Fuzzy Hashing and Genetic Algorithm-Based Memory Deduplication of Static Pages"
- **Authors**: N. Jagadeeswari, V. Mohanraj, Y. Suresh, J. Senthilkumar
- **Published**: Automatika, 2023, 64(4), 868-877

---

## 1. METHODOLOGY OVERVIEW

### Core Components

#### Phase 1: Offline Processing
1. **Application Clustering** (Fuzzy Hashing + Hierarchical Agglomerative Clustering)
   - Input: Applications from multiple VMs
   - Process: Identify similar applications using fuzzy hashing
   - Output: Clustered groups of similar applications

2. **Static Page Classification** (Genetic Algorithm)
   - Input: Code segments of clustered applications
   - Process: Detect similar pages using GA-based similarity detection
   - Output: Identified similar pages within each cluster

3. **Multilevel Shared Page Table** (MSPT)
   - Store metadata about shareable pages
   - Record similar content relationships
   - Create lookup tables for online phase

#### Phase 2: Online Processing
4. **Memory Deduplication**
   - Merge pages using pre-computed MSPT
   - Reduce memory capacity requirements
   - Apply copy-on-write protection

---

## 2. IMPLEMENTATION ARCHITECTURE

### System Components

```
┌─────────────────────────────────────────┐
│     Virtual Machine Instances           │
│  (Ubuntu 16.0 running various apps)    │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│        mSMD Deduplication Engine         │
├─────────────────────────────────────────┤
│  ┌─────────────────────────────────┐   │
│  │  1. Fuzzy Hashing Module        │   │ (Offline)
│  │     - Application similarity    │   │
│  └─────────────────────────────────┘   │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │  2. Genetic Algorithm Module    │   │ (Offline)
│  │     - Page similarity detection │   │
│  └─────────────────────────────────┘   │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │  3. Multilevel Shared Page Tbl  │   │ (Offline)
│  │     - Store dedup metadata      │   │
│  └─────────────────────────────────┘   │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │  4. Memory Deduplication        │   │ (Online)
│  │     - Merge pages               │   │
│  └─────────────────────────────────┘   │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│     Performance Metrics Collection      │
│  - Memory usage reduction               │
│  - Response time improvement            │
│  - CPU overhead reduction               │
└─────────────────────────────────────────┘
```

---

## 3. IMPLEMENTATION PHASES

### Phase 1: Environment Setup
1. Install KVM hypervisor and QEMU
2. Create Ubuntu 16.0 VM templates
3. Configure monitoring tools (perf, memory stats)
4. Set up workload tools (.NET, Apache, MySQL, Genymotion)

### Phase 2: Core Module Implementation
1. **Fuzzy Hashing Module**
   - Input: Application binaries
   - Algorithm: SSDEEP or similar
   - Output: Fuzzy hash fingerprints

2. **Hierarchical Agglomerative Clustering**
   - Input: Fuzzy hash values
   - Algorithm: Bottom-up clustering with similarity threshold (30%)
   - Output: Application clusters

3. **Genetic Algorithm Module**
   - Input: Code section pages (4KB each)
   - Algorithm: GA with fitness based on object dump comparison
   - Output: Similar page pairs

4. **Multilevel Shared Page Table**
   - Data structure: Hash table with VM and page info
   - Store: Similar page relationships and metadata

### Phase 3: Integration & Online Processing
1. Integrate all modules
2. Implement copy-on-write protection
3. Create page merging logic
4. Implement monitoring and metrics collection

### Phase 4: Testing & Validation
1. Run 4 workloads (described below)
2. Collect performance metrics
3. Compare against KSM baseline
4. Document results

---

## 4. EXPERIMENTAL SETUP

### Hardware Configuration
- **CPU**: Intel Core i5 (8th Gen) - or equivalent
- **RAM**: Minimum 16GB for host + VMs
- **Storage**: 50GB for VM images
- **OS**: Linux Ubuntu 20.04+ (with KVM support)

### Software Requirements
- KVM/QEMU
- Linux kernel with KSM enabled
- Python 3.8+ (for implementation)
- ssdeep (for fuzzy hashing)
- perf (for performance monitoring)

### Workloads

| Workload | Type | Command/Tool | Metric |
|----------|------|-------------|--------|
| .Net Application | Web App | dotnet framework | Page sharing rate |
| Apache Server | HTTP | ab with 24 concurrent requests | Response time |
| MySQL Database | Database | SysBench benchmark | Throughput |
| Genymotion | Android Emulator | Genymotion on VirtualBox | Memory usage |

---

## 5. EXPECTED RESULTS

Based on the paper's findings:

| Metric | Expected Improvement |
|--------|---------------------|
| Memory capacity reduction | 20-28% |
| Unnecessary comparisons reduction | 24.5-27.5% |
| Response time improvement | Significantly lower than KSM |
| CPU overhead | <1% |
| Page sharing efficiency | 25-30% higher |

---

## 6. IMPLEMENTATION TIMELINE

```
Week 1: Environment Setup
Week 2: Fuzzy Hashing & Clustering
Week 3: Genetic Algorithm & Page Classification
Week 4: Multilevel Page Table & Integration
Week 5: Testing with Workloads
Week 6: Results Collection & Documentation
```

---

## 7. DELIVERABLES

1. **Source Code**
   - Modular Python/C implementation
   - Well-documented with comments
   - Ready to deploy

2. **Configuration Files**
   - VM setup scripts
   - Workload configuration
   - Monitoring setup

3. **Experimental Results**
   - Performance metrics comparison
   - Screenshots/logs of execution
   - Graphs comparing mSMD vs KSM

4. **Implementation Report**
   - Methodology description
   - Challenges faced and solutions
   - Results analysis
   - Comparison with paper's findings

---

## 8. KEY ALGORITHMS (From Paper)

### Algorithm 1: Application Clustering
```
Input: Applications from multiple VMs
Output: Clusters of similar applications

For each pair of applications:
  - Compute fuzzy hash
  - If similarity > 30%: mark as candidates
  - Use agglomerative clustering to merge similar apps
```

### Algorithm 2: Static Page Similarity Detection
```
Input: Code section pages (4KB each)
Output: Similar pages identified

Process:
  - Generate initial population from candidate pages
  - Fitness evaluation using object dump comparison
  - Selection based on roulette wheel
  - Repeat until convergence
```

### Algorithm 3: Multilevel Shared Page Table
```
Input: Classified pages
Output: Shared page table entries

For each page:
  - Check if identical pages exist
  - Create entry if similar content found
  - Link to other shared pages
  - Store in multilevel table
```

### Algorithm 4: Memory Deduplication
```
Input: Running VMs with pages
Output: Merged memory pages

For each VM page:
  - Check if in shared page table
  - If found: merge with other shared pages
  - Apply copy-on-write protection
  - Update page table entry
```

---

## 9. MONITORING & METRICS

### Key Performance Indicators (KPIs)

1. **Memory Efficiency**
   - Total memory used (MB)
   - Pages shared (count)
   - Memory reduction percentage

2. **Performance**
   - Response time (ms)
   - Throughput (operations/sec)
   - Page fault rate

3. **CPU Overhead**
   - CPU cycles consumed
   - Context switches
   - System load

4. **Comparison Metrics**
   - Number of page comparisons
   - Reduction in unnecessary comparisons
   - Detection time (offline vs online)

---

## 10. TROUBLESHOOTING

Common issues and solutions:

1. **KVM not available**: Check BIOS virtualization settings
2. **Insufficient memory**: Reduce VM count or memory per VM
3. **Fuzzy hash mismatch**: Verify algorithm implementation
4. **GA convergence issues**: Tune mutation and crossover rates
5. **Page table overflow**: Increase MSPT size or optimize clustering

---

## References
1. Jagadeeswari, N., et al. (2023). "Optimization of Virtual Machines Performance Using Fuzzy Hashing and Genetic Algorithm." Automatika, 64(4), 868-877.
2. KVM Documentation: https://www.linux-kvm.org/
3. SSDEEP Fuzzy Hashing: https://ssdeep-project.github.io/ssdeep/
