#!/usr/bin/env python3
"""
mSMD Performance Visualization Module

Generates graphs similar to those in the paper:
- Figure 2: Performance increase with different Guest OS
- Figure 3: Performance for simultaneous VMs with same OS
- Figure 4: Physical memory pages' proportion for various times of shared
- Figure 5: Response time comparison (mSMD vs KSM)
- Figure 6: VMs average runtime
- Figure 7: Pages' sharing comparison (4 workloads)
- Figure 8: Percentage of reduction in unnecessary page comparison

Author: [Your Name]
Date: December 7, 2025
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Rectangle
import seaborn as sns
from datetime import datetime
import os

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Create output directory for graphs
OUTPUT_DIR = "results/graphs"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def save_figure(fig, filename, dpi=300):
    """Save figure with high quality"""
    filepath = os.path.join(OUTPUT_DIR, filename)
    fig.savefig(filepath, dpi=dpi, bbox_inches='tight')
    print(f"✓ Saved: {filepath}")


# ============================================================================
# FIGURE 2: Performance Increase with Different Guest OS
# ============================================================================

def generate_figure2_performance_different_os():
    """
    Normalized System Performance for different VM configurations
    with different Guest OS
    """
    configurations = ['1-VM-4G', '2-VM-4G', '4-VM-4G', '8-VM-4G',
                     '1-VM-8G', '2-VM-8G', '4-VM-8G', '8-VM-8G']
    
    # Sample data based on paper's findings
    # Normalized performance (>1.0 means improvement)
    performance = [1.02, 1.05, 1.10, 1.15, 1.03, 1.07, 1.12, 1.18]
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    bars = ax.bar(configurations, performance, color='steelblue', alpha=0.8, edgecolor='navy')
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    ax.axhline(y=1.0, color='red', linestyle='--', alpha=0.7, label='Baseline (No improvement)')
    ax.set_xlabel('VM Configuration', fontsize=12, fontweight='bold')
    ax.set_ylabel('Normalized System Performance', fontsize=12, fontweight='bold')
    ax.set_title('Figure 2: Performance Increase of Virtual Machines with Different Guest OS\n(mSMD Approach)',
                fontsize=14, fontweight='bold')
    ax.set_ylim([0.9, 1.25])
    ax.legend(loc='upper left')
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45, ha='right')
    
    save_figure(fig, 'figure2_performance_different_os.png')
    return fig


# ============================================================================
# FIGURE 3: Performance for Simultaneous VMs with Same OS
# ============================================================================

def generate_figure3_performance_same_os():
    """
    Normalized System Performance for VMs running same OS
    Shows higher improvement when OS is identical
    """
    configurations = ['1-VM-4G', '2-VM-4G', '4-VM-4G', '8-VM-4G',
                     '1-VM-8G', '2-VM-8G', '4-VM-8G', '8-VM-8G']
    
    # Higher performance with same OS (more similar pages)
    performance = [1.03, 1.08, 1.13, 1.18, 1.04, 1.10, 1.15, 1.20]
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    bars = ax.bar(configurations, performance, color='forestgreen', alpha=0.8, edgecolor='darkgreen')
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    ax.axhline(y=1.0, color='red', linestyle='--', alpha=0.7, label='Baseline')
    ax.set_xlabel('VM Configuration', fontsize=12, fontweight='bold')
    ax.set_ylabel('Normalized System Performance', fontsize=12, fontweight='bold')
    ax.set_title('Figure 3: Performance for Simultaneous VMs Running Same OS\n(Higher improvement due to more similar pages)',
                fontsize=14, fontweight='bold')
    ax.set_ylim([0.9, 1.3])
    ax.legend(loc='upper left')
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45, ha='right')
    
    save_figure(fig, 'figure3_performance_same_os.png')
    return fig


# ============================================================================
# FIGURE 4: Physical Memory Pages' Proportion for Various Times of Shared
# ============================================================================

def generate_figure4_shared_pages_proportion():
    """
    Shared times over memory pages shared vs number of scans
    for different VM counts
    """
    scans = [1, 2, 3, 4]
    
    # Shared times metric (decreases with more scans)
    vm1 = [0.95, 0.85, 0.78, 0.72]
    vm2 = [0.88, 0.75, 0.68, 0.62]
    vm4 = [0.80, 0.65, 0.58, 0.52]
    vm8 = [0.70, 0.55, 0.48, 0.42]
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    width = 0.2
    x = np.arange(len(scans))
    
    bars1 = ax.bar(x - 1.5*width, vm1, width, label='1 VM', color='#FF6B6B', alpha=0.8)
    bars2 = ax.bar(x - 0.5*width, vm2, width, label='2 VMs', color='#4ECDC4', alpha=0.8)
    bars3 = ax.bar(x + 0.5*width, vm4, width, label='4 VMs', color='#45B7D1', alpha=0.8)
    bars4 = ax.bar(x + 1.5*width, vm8, width, label='8 VMs', color='#FFA07A', alpha=0.8)
    
    ax.set_xlabel('Number of Scans', fontsize=12, fontweight='bold')
    ax.set_ylabel('Shared Times over Memory Pages Shared', fontsize=12, fontweight='bold')
    ax.set_title('Figure 4: Physical Memory Pages\' Proportion for Various Times of Shared\n(More VMs = More sharing opportunities)',
                fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(scans)
    ax.legend(loc='upper right', fontsize=11)
    ax.grid(True, alpha=0.3, axis='y')
    
    save_figure(fig, 'figure4_shared_pages_proportion.png')
    return fig


# ============================================================================
# FIGURE 5: Response Time Comparison (mSMD vs KSM)
# ============================================================================

def generate_figure5_response_time():
    """
    Response time comparison: mSMD vs traditional KSM
    mSMD shows significantly lower response time
    """
    configurations = ['1-VM-4G', '2-VM-4G', '4-VM-4G', '8-VM-4G',
                     '1-VM-8G', '2-VM-8G', '4-VM-8G', '8-VM-8G']
    
    # Response time in arbitrary units (lower is better)
    ksm_time = [120, 145, 180, 220, 115, 140, 175, 210]
    msmd_time = [85, 95, 110, 135, 80, 90, 105, 125]
    
    fig, ax = plt.subplots(figsize=(14, 7))
    
    x = np.arange(len(configurations))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, ksm_time, width, label='KSM (Traditional)', 
                   color='#E74C3C', alpha=0.8, edgecolor='darkred')
    bars2 = ax.bar(x + width/2, msmd_time, width, label='mSMD (Proposed)', 
                   color='#27AE60', alpha=0.8, edgecolor='darkgreen')
    
    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom', fontsize=9)
    
    ax.set_xlabel('VM Configuration', fontsize=12, fontweight='bold')
    ax.set_ylabel('Response Time (arbitrary units)', fontsize=12, fontweight='bold')
    ax.set_title('Figure 5: Response Time Comparison\n(mSMD shows significantly lower response time than KSM)',
                fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(configurations)
    ax.legend(loc='upper left', fontsize=11)
    ax.grid(True, alpha=0.3, axis='y')
    plt.xticks(rotation=45, ha='right')
    
    save_figure(fig, 'figure5_response_time_comparison.png')
    return fig


# ============================================================================
# FIGURE 6: VMs Average Runtime
# ============================================================================

def generate_figure6_average_runtime():
    """
    Average runtime comparison between KSM and mSMD
    mSMD shows consistently shorter runtime
    """
    configurations = ['1-VM-4G', '2-VM-4G', '4-VM-4G', '8-VM-4G',
                     '1-VM-8G', '2-VM-8G', '4-VM-8G', '8-VM-8G']
    
    # Runtime in arbitrary units
    ksm_runtime = [155, 175, 195, 225, 145, 165, 185, 215]
    msmd_runtime = [130, 145, 160, 180, 125, 140, 155, 170]
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    x = np.arange(len(configurations))
    
    ax.plot(x, ksm_runtime, marker='o', linewidth=2.5, markersize=8, 
            label='KSM', color='#E74C3C', linestyle='--')
    ax.plot(x, msmd_runtime, marker='s', linewidth=2.5, markersize=8, 
            label='mSMD', color='#27AE60', linestyle='-')
    
    # Add value labels
    for i, (ksm_val, msmd_val) in enumerate(zip(ksm_runtime, msmd_runtime)):
        ax.text(i, ksm_val + 5, f'{ksm_val}', ha='center', fontsize=9, color='#E74C3C')
        ax.text(i, msmd_val - 10, f'{msmd_val}', ha='center', fontsize=9, color='#27AE60')
    
    ax.set_xlabel('VM Configuration', fontsize=12, fontweight='bold')
    ax.set_ylabel('Virtual Machines Average Runtime (arbitrary units)', fontsize=12, fontweight='bold')
    ax.set_title('Figure 6: VMs Average Runtime Comparison\n(mSMD shows shorter runtime across all configurations)',
                fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(configurations)
    ax.legend(loc='upper left', fontsize=11)
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45, ha='right')
    
    save_figure(fig, 'figure6_average_runtime.png')
    return fig


# ============================================================================
# FIGURE 7: Pages' Sharing Comparison (4 Workloads)
# ============================================================================

def generate_figure7_pages_sharing():
    """
    Pages sharing over time for 4 different workloads
    Shows mSMD detects significantly more shared pages
    """
    time_points = np.arange(0, 600, 10)  # Time in seconds (x100)
    
    # Simulate page sharing growth over time
    # mSMD detects more pages faster
    
    # .NET Application
    ksm_dotnet = 50 + 300 * (1 - np.exp(-time_points/200))
    msmd_dotnet = 80 + 500 * (1 - np.exp(-time_points/150))
    
    # Apache Server
    ksm_apache = 60 + 280 * (1 - np.exp(-time_points/180))
    msmd_apache = 90 + 480 * (1 - np.exp(-time_points/140))
    
    # MySQL Database
    ksm_mysql = 55 + 290 * (1 - np.exp(-time_points/190))
    msmd_mysql = 85 + 490 * (1 - np.exp(-time_points/145))
    
    # Genymotion
    ksm_genymotion = 45 + 270 * (1 - np.exp(-time_points/200))
    msmd_genymotion = 75 + 470 * (1 - np.exp(-time_points/155))
    
    # Create 2x2 subplot
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # (a) .NET Application
    ax1.plot(time_points/100, ksm_dotnet, label='KSM', color='#E74C3C', linewidth=2, linestyle='--')
    ax1.plot(time_points/100, msmd_dotnet, label='mSMD', color='#27AE60', linewidth=2)
    ax1.set_xlabel('Time (seconds × 100)', fontsize=11, fontweight='bold')
    ax1.set_ylabel('No. of pages sharing', fontsize=11, fontweight='bold')
    ax1.set_title('(a) .NET Application', fontsize=12, fontweight='bold')
    ax1.legend(loc='lower right', fontsize=10)
    ax1.grid(True, alpha=0.3)
    
    # (b) Apache HTTP Server
    ax2.plot(time_points/100, ksm_apache, label='KSM', color='#E74C3C', linewidth=2, linestyle='--')
    ax2.plot(time_points/100, msmd_apache, label='mSMD', color='#27AE60', linewidth=2)
    ax2.set_xlabel('Time (seconds × 100)', fontsize=11, fontweight='bold')
    ax2.set_ylabel('No. of pages sharing', fontsize=11, fontweight='bold')
    ax2.set_title('(b) Apache HTTP Server', fontsize=12, fontweight='bold')
    ax2.legend(loc='lower right', fontsize=10)
    ax2.grid(True, alpha=0.3)
    
    # (c) MySQL Database
    ax3.plot(time_points/100, ksm_mysql, label='KSM', color='#E74C3C', linewidth=2, linestyle='--')
    ax3.plot(time_points/100, msmd_mysql, label='mSMD', color='#27AE60', linewidth=2)
    ax3.set_xlabel('Time (seconds × 100)', fontsize=11, fontweight='bold')
    ax3.set_ylabel('No. of pages sharing', fontsize=11, fontweight='bold')
    ax3.set_title('(c) MySQL Database', fontsize=12, fontweight='bold')
    ax3.legend(loc='lower right', fontsize=10)
    ax3.grid(True, alpha=0.3)
    
    # (d) Genymotion
    ax4.plot(time_points/100, ksm_genymotion, label='KSM', color='#E74C3C', linewidth=2, linestyle='--')
    ax4.plot(time_points/100, msmd_genymotion, label='mSMD', color='#27AE60', linewidth=2)
    ax4.set_xlabel('Time (seconds × 100)', fontsize=11, fontweight='bold')
    ax4.set_ylabel('No. of pages sharing', fontsize=11, fontweight='bold')
    ax4.set_title('(d) Genymotion', fontsize=12, fontweight='bold')
    ax4.legend(loc='lower right', fontsize=10)
    ax4.grid(True, alpha=0.3)
    
    fig.suptitle('Figure 7: Pages\' Sharing Comparison for Four Workloads\n(mSMD detects significantly more shared pages over time)',
                fontsize=14, fontweight='bold', y=0.995)
    
    plt.tight_layout()
    save_figure(fig, 'figure7_pages_sharing_comparison.png')
    return fig


# ============================================================================
# FIGURE 8: Percentage of Reduction in Unnecessary Page Comparison
# ============================================================================

def generate_figure8_comparison_reduction():
    """
    Percentage of futile comparison reduction for 4 workloads
    Shows ~24-27% reduction achieved by mSMD
    """
    workloads = ['.NET Application', 'Apache HTTP\nServer', 'MySQL\nDatabase', 'Genymotion']
    
    # Reduction percentages (as reported in paper)
    reduction = [24.5, 27.5, 26.0, 25.8]
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    colors = ['#3498DB', '#E74C3C', '#2ECC71', '#F39C12']
    bars = ax.bar(workloads, reduction, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    
    # Add value labels
    for bar, val in zip(bars, reduction):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.1f}%',
                ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    ax.set_ylabel('Percentage of Futile Comparison Reduction (%)', fontsize=12, fontweight='bold')
    ax.set_title('Figure 8: Percentage of Reduction in Unnecessary Page Comparison\n(mSMD achieves ~24-27% reduction across workloads)',
                fontsize=14, fontweight='bold')
    ax.set_ylim([0, 35])
    ax.grid(True, alpha=0.3, axis='y')
    
    # Add horizontal line for average
    avg_reduction = np.mean(reduction)
    ax.axhline(y=avg_reduction, color='red', linestyle='--', alpha=0.7, 
               label=f'Average: {avg_reduction:.1f}%')
    ax.legend(loc='upper right', fontsize=11)
    
    save_figure(fig, 'figure8_comparison_reduction.png')
    return fig


# ============================================================================
# BONUS: Summary Dashboard
# ============================================================================

def generate_summary_dashboard():
    """
    Create a summary dashboard with key metrics
    """
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(3, 3, hspace=0.4, wspace=0.3)
    
    # Title
    fig.suptitle('mSMD Implementation - Performance Summary Dashboard', 
                 fontsize=16, fontweight='bold', y=0.98)
    
    # 1. Memory Reduction (top left)
    ax1 = fig.add_subplot(gs[0, 0])
    categories = ['Expected\n(Paper)', 'Achieved\n(Your Results)']
    values = [25, 0]  # Fill with your actual results
    colors = ['#3498DB', '#2ECC71']
    bars = ax1.bar(categories, values, color=colors, alpha=0.8, edgecolor='black')
    ax1.set_ylabel('Memory Reduction (%)', fontweight='bold')
    ax1.set_title('Memory Reduction', fontweight='bold')
    ax1.set_ylim([0, 35])
    ax1.grid(True, alpha=0.3, axis='y')
    
    # 2. Comparison Reduction (top middle)
    ax2 = fig.add_subplot(gs[0, 1])
    categories = ['Expected\n(Paper)', 'Achieved\n(Your Results)']
    values = [27, 0]  # Fill with your actual results
    colors = ['#E74C3C', '#F39C12']
    bars = ax2.bar(categories, values, color=colors, alpha=0.8, edgecolor='black')
    ax2.set_ylabel('Comparison Reduction (%)', fontweight='bold')
    ax2.set_title('Unnecessary Comparisons', fontweight='bold')
    ax2.set_ylim([0, 35])
    ax2.grid(True, alpha=0.3, axis='y')
    
    # 3. CPU Overhead (top right)
    ax3 = fig.add_subplot(gs[0, 2])
    categories = ['Expected\n(Paper)', 'Achieved\n(Your Results)']
    values = [0.8, 0]  # Fill with your actual results
    colors = ['#9B59B6', '#1ABC9C']
    bars = ax3.bar(categories, values, color=colors, alpha=0.8, edgecolor='black')
    ax3.set_ylabel('CPU Overhead (%)', fontweight='bold')
    ax3.set_title('CPU Overhead per VM', fontweight='bold')
    ax3.set_ylim([0, 5])
    ax3.axhline(y=1, color='red', linestyle='--', alpha=0.7, label='Target: <1%')
    ax3.legend(fontsize=9)
    ax3.grid(True, alpha=0.3, axis='y')
    
    # 4. Performance by Configuration (middle row, span 2 columns)
    ax4 = fig.add_subplot(gs[1, :2])
    configs = ['1-VM-4G', '2-VM-4G', '4-VM-4G', '8-VM-4G', '8-VM-8G']
    performance = [1.02, 1.05, 1.10, 1.15, 1.18]
    ax4.plot(configs, performance, marker='o', linewidth=3, markersize=10, 
            color='#27AE60', label='mSMD Performance')
    ax4.axhline(y=1.0, color='red', linestyle='--', alpha=0.7, label='Baseline')
    ax4.set_ylabel('Normalized Performance', fontweight='bold')
    ax4.set_xlabel('VM Configuration', fontweight='bold')
    ax4.set_title('System Performance by Configuration', fontweight='bold')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    plt.setp(ax4.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    # 5. Workload Comparison (middle right)
    ax5 = fig.add_subplot(gs[1, 2])
    workloads = ['.NET', 'Apache', 'MySQL', 'Genymotion']
    sharing = [580, 570, 575, 545]
    ax5.barh(workloads, sharing, color=['#3498DB', '#E74C3C', '#2ECC71', '#F39C12'], 
            alpha=0.8, edgecolor='black')
    ax5.set_xlabel('Pages Shared', fontweight='bold')
    ax5.set_title('Page Sharing by Workload', fontweight='bold')
    ax5.grid(True, alpha=0.3, axis='x')
    
    # 6. Key Statistics Table (bottom row)
    ax6 = fig.add_subplot(gs[2, :])
    ax6.axis('off')
    
    table_data = [
        ['Metric', 'Expected (Paper)', 'Your Result', 'Status'],
        ['Memory Reduction', '20-28%', 'TBD', '⏳ Pending'],
        ['Comparison Reduction', '24.5-27.5%', 'TBD', '⏳ Pending'],
        ['Response Time Improvement', 'Significant', 'TBD', '⏳ Pending'],
        ['CPU Overhead', '<1% per VM', 'TBD', '⏳ Pending'],
        ['Page Sharing Efficiency', '25-30% higher', 'TBD', '⏳ Pending'],
    ]
    
    table = ax6.table(cellText=table_data, cellLoc='center', loc='center',
                     colWidths=[0.3, 0.25, 0.25, 0.2])
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2)
    
    # Style header row
    for i in range(4):
        cell = table[(0, i)]
        cell.set_facecolor('#34495E')
        cell.set_text_props(weight='bold', color='white')
    
    # Alternate row colors
    for i in range(1, 6):
        for j in range(4):
            cell = table[(i, j)]
            if i % 2 == 0:
                cell.set_facecolor('#ECF0F1')
            else:
                cell.set_facecolor('#FFFFFF')
    
    ax6.set_title('Key Performance Metrics Summary', fontweight='bold', fontsize=12, pad=20)
    
    save_figure(fig, 'summary_dashboard.png')
    return fig


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def generate_all_figures():
    """Generate all figures from the paper"""
    
    print("\n" + "="*80)
    print("mSMD Performance Visualization")
    print("Generating all figures from the research paper...")
    print("="*80 + "\n")
    
    figures = []
    
    print("[1/9] Generating Figure 2: Performance with Different OS...")
    figures.append(generate_figure2_performance_different_os())
    
    print("[2/9] Generating Figure 3: Performance with Same OS...")
    figures.append(generate_figure3_performance_same_os())
    
    print("[3/9] Generating Figure 4: Shared Pages Proportion...")
    figures.append(generate_figure4_shared_pages_proportion())
    
    print("[4/9] Generating Figure 5: Response Time Comparison...")
    figures.append(generate_figure5_response_time())
    
    print("[5/9] Generating Figure 6: Average Runtime...")
    figures.append(generate_figure6_average_runtime())
    
    print("[6/9] Generating Figure 7: Pages Sharing (4 workloads)...")
    figures.append(generate_figure7_pages_sharing())
    
    print("[7/9] Generating Figure 8: Comparison Reduction...")
    figures.append(generate_figure8_comparison_reduction())
    
    print("[8/9] Generating Summary Dashboard...")
    figures.append(generate_summary_dashboard())
    
    print("[9/9] Creating results summary...")
    create_results_summary()
    
    print("\n" + "="*80)
    print(f"✓ All figures generated successfully!")
    print(f"✓ Output directory: {OUTPUT_DIR}")
    print("="*80 + "\n")
    
    print("Generated files:")
    for filename in sorted(os.listdir(OUTPUT_DIR)):
        if filename.endswith('.png'):
            print(f"  • {filename}")
    
    print("\nYou can now:")
    print("  1. View the graphs in the results/graphs/ folder")
    print("  2. Include them in your Implementation Report")
    print("  3. Compare with your actual experimental results")
    print("  4. Update the dashboard with your real data\n")
    
    return figures


def create_results_summary():
    """Create a text summary of expected results"""
    summary_file = os.path.join(OUTPUT_DIR, 'RESULTS_SUMMARY.txt')
    
    with open(summary_file, 'w') as f:
        f.write("="*80 + "\n")
        f.write("mSMD Implementation - Expected Results Summary\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*80 + "\n\n")
        
        f.write("FIGURE 2: Performance Increase (Different Guest OS)\n")
        f.write("-" * 50 + "\n")
        f.write("Configuration    | Normalized Performance\n")
        f.write("-" * 50 + "\n")
        f.write("1-VM-4G          | 1.02\n")
        f.write("2-VM-4G          | 1.05\n")
        f.write("4-VM-4G          | 1.10\n")
        f.write("8-VM-4G          | 1.15\n")
        f.write("1-VM-8G          | 1.03\n")
        f.write("2-VM-8G          | 1.07\n")
        f.write("4-VM-8G          | 1.12\n")
        f.write("8-VM-8G          | 1.18 (Best performance)\n")
        f.write("\n")
        
        f.write("FIGURE 5: Response Time Comparison\n")
        f.write("-" * 50 + "\n")
        f.write("mSMD shows 30-40% lower response time than KSM\n")
        f.write("across all configurations\n")
        f.write("\n")
        
        f.write("FIGURE 8: Unnecessary Comparison Reduction\n")
        f.write("-" * 50 + "\n")
        f.write("Workload             | Reduction %\n")
        f.write("-" * 50 + "\n")
        f.write(".NET Application     | 24.5%\n")
        f.write("Apache HTTP Server   | 27.5%\n")
        f.write("MySQL Database       | 26.0%\n")
        f.write("Genymotion          | 25.8%\n")
        f.write("Average             | ~26.0%\n")
        f.write("\n")
        
        f.write("KEY FINDINGS:\n")
        f.write("-" * 50 + "\n")
        f.write("1. Memory Reduction: 20-28% (target: ~25%)\n")
        f.write("2. Response Time: Significantly better than KSM\n")
        f.write("3. CPU Overhead: <1% per VM\n")
        f.write("4. Best Performance: 8-VMs with 8GB memory\n")
        f.write("5. Same OS VMs: Higher performance improvement\n")
        f.write("\n")
        
        f.write("NEXT STEPS:\n")
        f.write("-" * 50 + "\n")
        f.write("1. Run your actual experiments\n")
        f.write("2. Replace sample data with real measurements\n")
        f.write("3. Compare your results with these expected values\n")
        f.write("4. Update the summary dashboard with actual data\n")
        f.write("5. Include graphs in your Implementation Report\n")
        f.write("\n")
    
    print(f"✓ Saved: {summary_file}")


if __name__ == "__main__":
    # Generate all figures
    figures = generate_all_figures()
    
    # Optional: Display the figures
    print("\nPress Enter to close all figures...")
    plt.show()
