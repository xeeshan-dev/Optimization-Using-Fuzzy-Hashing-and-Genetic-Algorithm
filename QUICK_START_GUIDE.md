# mSMD Implementation - Quick Start Guide

## Overview

This guide provides step-by-step instructions to get started with the mSMD implementation.

---

## STEP 1: Environment Prerequisites

### Option A: Linux with KVM Support (Recommended)

Check if your system supports virtualization:

```bash
# Check CPU virtualization support
grep -c "vmx\|svm" /proc/cpuinfo

# Check if KVM is available
kvm-ok

# Install required packages
sudo apt-get update
sudo apt-get install -y \
    qemu-kvm \
    libvirt-daemon-system \
    libvirt-clients \
    bridge-utils \
    virt-manager \
    linux-image-generic \
    linux-headers-generic
```

### Option B: Docker-based Simulation (Alternative)

If you don't have a Linux machine, use Docker for a simulation environment:

```bash
docker pull ubuntu:latest
docker run -it ubuntu:latest /bin/bash
apt-get update && apt-get install -y python3 python3-pip
```

---

## STEP 2: Install Python Dependencies

### Create Virtual Environment

```bash
python3 -m venv mSMD_env
source mSMD_env/bin/activate  # On Windows: mSMD_env\Scripts\activate
```

### Install Packages

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### requirements.txt

```
# For fuzzy hashing
ssdeep-python==3.4

# For data processing
numpy==1.21.0
pandas==1.3.0

# For genetic algorithms
deap==1.3.1

# Utilities
matplotlib==3.4.2
json5==0.9.6
```

---

## STEP 3: Download and Setup Implementation

### Clone or Download

```bash
# Download the implementation files
# Files: msmd_implementation.py, IMPLEMENTATION_GUIDE.md

cd /path/to/mSMD_project
ls -la
```

### Verify Files

```bash
# Should have:
# - msmd_implementation.py (Core implementation)
# - IMPLEMENTATION_GUIDE.md (Detailed guide)
# - papper 2.pdf (Original paper)
```

---

## STEP 4: Run Sample Implementation

### Test Basic Functionality

```bash
cd /path/to/mSMD_project
python3 msmd_implementation.py
```

**Expected Output:**

```
╔════════════════════════════════════════════════════════════════════════════╗
║                   mSMD COMPLETE PIPELINE EXECUTION                        ║
╚════════════════════════════════════════════════════════════════════════════╝

2025-12-07 10:15:30,123 - msmd_implementation.root - INFO - ================================================================================
2025-12-07 10:15:30,123 - msmd_implementation.root - INFO - OFFLINE PROCESSING PHASE
2025-12-07 10:15:30,123 - msmd_implementation.root - INFO - ================================================================================

2025-12-07 10:15:30,124 - msmd_implementation.FuzzyHashingModule - INFO - Starting clustering of 3 applications
2025-12-07 10:15:30,126 - msmd_implementation.FuzzyHashingModule - INFO - Clustering complete. Created 2 clusters

[... more output ...]

================================================================================
EXECUTION SUMMARY
================================================================================
total_applications.....................3
application_clusters...................2
similar_page_pairs.....................3
mspt_entries...........................3
memory_saved_mb........................0.00
pages_merged...........................3
```

---

## STEP 5: Test Individual Modules

### Test 1: Fuzzy Hashing Module

Create file `test_fuzzy_hashing.py`:

```python
from msmd_implementation import FuzzyHashingModule, Application

# Initialize module
fm = FuzzyHashingModule()

# Test fuzzy hashing
hash1 = fm.compute_fuzzy_hash(b"Binary content of application 1")
hash2 = fm.compute_fuzzy_hash(b"Binary content of application 2")

print(f"Hash 1: {hash1}")
print(f"Hash 2: {hash2}")

# Test similarity calculation
similarity = fm.calculate_similarity(hash1, hash2)
print(f"Similarity: {similarity:.2f}%")

# Test clustering
apps = [
    Application(1, 1, "App1", hash1),
    Application(2, 1, "App2", hash2),
]

clusters = fm.cluster_applications(apps)
print(f"Clusters formed: {clusters}")
```

Run:
```bash
python3 test_fuzzy_hashing.py
```

---

### Test 2: Genetic Algorithm Module

Create file `test_genetic_algorithm.py`:

```python
from msmd_implementation import GeneticAlgorithmModule, Page

# Initialize module
ga = GeneticAlgorithmModule(population_size=30, generations=10)

# Create sample pages
pages = [
    Page(1, 1, 1, "hash1", "dump1" * 100),
    Page(2, 1, 1, "hash2", "dump1" * 100),  # Similar
    Page(3, 1, 1, "hash3", "dump2" * 100),
    Page(4, 1, 1, "hash4", "dump1" * 100),  # Similar to 1,2
]

# Detect similar pages
similar_pairs = ga.detect_similar_pages(pages)

print(f"Found {len(similar_pairs)} similar page pairs:")
for page_id1, page_id2, similarity in similar_pairs:
    print(f"  Pages {page_id1}, {page_id2}: {similarity:.2f}% similarity")
```

Run:
```bash
python3 test_genetic_algorithm.py
```

---

### Test 3: Multilevel Shared Page Table

Create file `test_mspt.py`:

```python
from msmd_implementation import MultilevelSharedPageTable, Page

# Initialize MSPT
mspt = MultilevelSharedPageTable()

# Create sample pages
pages = [
    Page(1, 1, 1, "hash1", "dump1"),
    Page(2, 1, 1, "hash2", "dump1"),
    Page(3, 1, 1, "hash3", "dump1"),
]

# Simulated similar pairs
similar_pairs = [(1, 2, 95.5), (2, 3, 87.2)]

# Build table
entries = mspt.build_table(pages, similar_pairs)
print(f"Created {entries} MSPT entries")

# Test lookup
entry = mspt.lookup(1)
if entry:
    print(f"Page 1 shareable with: {entry.similar_pages}")
else:
    print("Page 1 not found in MSPT")
```

Run:
```bash
python3 test_mspt.py
```

---

## STEP 6: KVM Environment Setup (Optional)

If you want to set up actual VM simulation:

### Create VM Image

```bash
# Download Ubuntu 16.04 LTS
wget http://releases.ubuntu.com/16.04/ubuntu-16.04.7-server-amd64.iso

# Create VM disk
qemu-img create -f qcow2 ubuntu-vm1.qcow2 20G

# Launch VM
qemu-system-x86_64 -m 2048 -cpu host -enable-kvm \
    -drive file=ubuntu-vm1.qcow2,if=virtio \
    -cdrom ubuntu-16.04.7-server-amd64.iso \
    -net nic,model=virtio -net user \
    -display gtk
```

### Alternative: Using virt-manager (GUI)

```bash
# Install virt-manager
sudo apt-get install virt-manager

# Launch GUI
virt-manager
```

---

## STEP 7: Create Experimental Workloads

### Sample 1: .NET Application Simulation

Create file `workload_dotnet.py`:

```python
import subprocess
import time

def run_dotnet_workload():
    """Simulate .NET application workload"""
    print("Starting .NET application workload...")
    
    # In real scenario, would run actual .NET app
    # For now, simulate with memory allocation
    
    data = bytearray(100 * 1024 * 1024)  # 100MB
    for i in range(len(data)):
        data[i] = i % 256
    
    time.sleep(5)
    print("Workload complete")

if __name__ == "__main__":
    run_dotnet_workload()
```

---

### Sample 2: Memory-Intensive Workload

Create file `workload_memory.py`:

```python
import random
import time

def memory_intensive_workload(duration=10, memory_mb=500):
    """Memory-intensive workload"""
    print(f"Starting memory workload: {memory_mb}MB for {duration}s")
    
    # Allocate memory
    data = bytearray(memory_mb * 1024 * 1024)
    
    # Access pattern (simulates real workload)
    for _ in range(duration * 10):
        idx = random.randint(0, len(data) - 1)
        data[idx] = random.randint(0, 255)
        time.sleep(0.1)
    
    print("Memory workload complete")

if __name__ == "__main__":
    memory_intensive_workload(duration=10, memory_mb=500)
```

---

## STEP 8: Run Full Experiment

### Create Experiment Script

Create file `run_experiment.py`:

```python
from msmd_implementation import mSMDOrchestrator, Page
import json
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'experiment_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)

def prepare_test_data():
    """Prepare sample application and page data"""
    
    # Sample applications
    app_contents = {
        1: b"App1_binary_content_section1" * 100,
        2: b"App1_binary_content_section1" * 100,  # Similar to App1
        3: b"App2_binary_content_section2" * 100,
        4: b"App3_binary_content_section3" * 100,
    }
    
    # Application pages for offline processing
    app_pages = {
        1: [
            Page(1, 1, 1, "hash1a", "dump1" * 50),
            Page(2, 1, 1, "hash1b", "dump1" * 50),
            Page(3, 1, 1, "hash1c", "dump2" * 50),
        ],
        2: [
            Page(4, 1, 2, "hash2a", "dump1" * 50),  # Similar to App1
            Page(5, 1, 2, "hash2b", "dump1" * 50),
        ],
        3: [
            Page(6, 1, 3, "hash3a", "dump3" * 50),
            Page(7, 1, 3, "hash3b", "dump4" * 50),
        ],
        4: [
            Page(8, 1, 4, "hash4a", "dump5" * 50),
        ],
    }
    
    # VM pages for online processing
    vm_pages = {
        1: [Page(1, 1, 1, "hash1a", "dump1" * 50), Page(4, 1, 2, "hash2a", "dump1" * 50)],
        2: [Page(2, 1, 1, "hash1b", "dump1" * 50), Page(5, 1, 2, "hash2b", "dump1" * 50)],
        3: [Page(3, 1, 1, "hash1c", "dump2" * 50), Page(6, 1, 3, "hash3a", "dump3" * 50)],
    }
    
    return app_contents, app_pages, vm_pages

def main():
    print("=" * 80)
    print("mSMD COMPLETE EXPERIMENT")
    print("=" * 80)
    
    # Prepare data
    app_contents, app_pages, vm_pages = prepare_test_data()
    
    # Run pipeline
    orchestrator = mSMDOrchestrator()
    results = orchestrator.run_complete_pipeline(app_contents, app_pages, vm_pages)
    
    # Print summary
    orchestrator.print_summary()
    
    # Save results
    output_file = f'results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    with open(output_file, 'w') as f:
        json.dump(results['summary'], f, indent=2)
    
    print(f"\nResults saved to: {output_file}")
    
    return results

if __name__ == "__main__":
    results = main()
```

Run:
```bash
python3 run_experiment.py
```

---

## STEP 9: Monitor and Analyze Results

### View Results

```bash
# View latest log
tail -f experiment_*.log

# View JSON results
cat results_*.json | python3 -m json.tool

# Generate summary
python3 << 'EOF'
import json
import glob

for result_file in sorted(glob.glob('results_*.json'))[-1:]:
    with open(result_file) as f:
        data = json.load(f)
    
    print("Memory Deduplication Results:")
    print(f"  Total Applications: {data['total_applications']}")
    print(f"  Application Clusters: {data['application_clusters']}")
    print(f"  Similar Page Pairs: {data['similar_page_pairs']}")
    print(f"  MSPT Entries: {data['mspt_entries']}")
    print(f"  Pages Merged: {data['pages_merged']}")
    print(f"  Memory Saved: {data['memory_saved_mb']:.2f} MB")
EOF
```

---

## STEP 10: Generate Implementation Report

Create file `generate_report.py`:

```python
from datetime import datetime
import json
import glob

def generate_report():
    """Generate implementation report"""
    
    report = f"""
# mSMD Implementation Report

**Date:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Results Summary

"""
    
    # Add results from latest run
    for result_file in sorted(glob.glob('results_*.json'))[-1:]:
        with open(result_file) as f:
            data = json.load(f)
        
        report += f"""
### Memory Deduplication Results

- Total Applications: {data['total_applications']}
- Application Clusters: {data['application_clusters']}
- Similar Page Pairs Detected: {data['similar_page_pairs']}
- MSPT Entries Created: {data['mspt_entries']}
- Pages Merged: {data['pages_merged']}
- Total Memory Saved: {data['memory_saved_mb']:.2f} MB

### Comparison with Paper's Findings

- Paper's Expected Memory Reduction: 20-28%
- Our Results: [Fill based on actual results]
- Status: [ACHIEVED / PARTIALLY ACHIEVED / NEEDS IMPROVEMENT]

## Conclusion

The mSMD implementation successfully demonstrated the feasibility of the proposed 
approach for memory deduplication in virtualized environments using fuzzy hashing 
and genetic algorithms.

"""
    
    # Save report
    report_file = f'IMPLEMENTATION_REPORT_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
    with open(report_file, 'w') as f:
        f.write(report)
    
    print(f"Report generated: {report_file}")
    return report_file

if __name__ == "__main__":
    generate_report()
```

Run:
```bash
python3 generate_report.py
```

---

## Troubleshooting

### Issue 1: Module Import Errors

```bash
# Solution: Ensure you're in the virtual environment
source mSMD_env/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue 2: Permission Denied

```bash
# Solution: Make script executable
chmod +x msmd_implementation.py

# Run with python3
python3 msmd_implementation.py
```

### Issue 3: KVM Not Available

```bash
# Solution: Check CPU support
grep -c "vmx\|svm" /proc/cpuinfo

# If output is 0, virtualization is not supported
# Alternative: Use Docker-based simulation
```

---

## Next Steps

1. ✅ Run sample implementation
2. ✅ Test individual modules
3. ✅ Set up KVM environment (optional)
4. ✅ Run full experiment
5. ✅ Analyze results
6. ✅ Complete implementation report
7. ✅ Prepare presentation

---

## References

- Original Paper: Jagadeeswari et al. (2023), Automatika, 64(4), 868-877
- KVM Documentation: https://www.linux-kvm.org/
- Python Genetic Algorithms: https://deap.readthedocs.io/

---

**Happy Implementing!** 🚀

