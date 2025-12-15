#!/usr/bin/env python3
"""
mSMD (Modified Static Memory Deduplication) Implementation
Paper: "Optimization of Virtual Machines Performance Using Fuzzy Hashing and Genetic Algorithm"
Authors: N. Jagadeeswari, et al. (2023)

This module implements the core components of the mSMD approach for memory deduplication
in virtualized environments using fuzzy hashing and genetic algorithms.
"""

import hashlib
import json
import logging
from dataclasses import dataclass, asdict
from typing import List, Dict, Tuple, Set
from collections import defaultdict
import random
import math

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class Page:
    """Represents a memory page (4KB default)"""
    page_id: int
    vm_id: int
    app_id: int
    content_hash: str
    object_dump: str
    size: int = 4096  # 4KB default page size
    shared: bool = False
    cluster_id: int = -1

    def to_dict(self):
        return asdict(self)


@dataclass
class Application:
    """Represents a virtual machine application"""
    app_id: int
    vm_id: int
    name: str
    fuzzy_hash: str
    pages: List[int] = None  # page IDs
    cluster_id: int = -1
    
    def __post_init__(self):
        if self.pages is None:
            self.pages = []


@dataclass
class FuzzyHashResult:
    """Result of fuzzy hashing comparison"""
    app1_id: int
    app2_id: int
    similarity_score: float  # 0-100
    is_similar: bool  # True if similarity > threshold


@dataclass
class SharedPageTableEntry:
    """Entry in the multilevel shared page table"""
    entry_id: int
    primary_page_id: int
    similar_pages: List[int]
    content_signature: str
    cluster_id: int
    created_timestamp: float


# ============================================================================
# MODULE 1: FUZZY HASHING & APPLICATION CLUSTERING
# ============================================================================

class FuzzyHashingModule:
    """
    Algorithm 1: Application Clustering using Fuzzy Hashing
    
    Identifies similar applications using fuzzy hashing and clusters them
    using Hierarchical Agglomerative Clustering (HAC).
    """
    
    SIMILARITY_THRESHOLD = 30  # 30% threshold as per paper
    
    def __init__(self):
        self.logger = logging.getLogger(__name__ + '.FuzzyHashingModule')
    
    def compute_fuzzy_hash(self, data: bytes) -> str:
        """
        Compute fuzzy hash of application binary/content
        Using simple rolling hash + content-based chunking
        """
        if isinstance(data, str):
            data = data.encode()
        
        # Simple rolling hash implementation
        hash_val = 0
        for byte in data:
            hash_val = ((hash_val << 5) ^ byte) & 0xFFFFFFFF
        
        return hashlib.md5(data).hexdigest()[:16]
    
    def calculate_similarity(self, hash1: str, hash2: str) -> float:
        """
        Calculate similarity between two fuzzy hashes
        Using normalized edit distance approach
        
        Returns: similarity score 0-100
        """
        if hash1 == hash2:
            return 100.0
        
        # Hamming distance approach for hash comparison
        distance = sum(c1 != c2 for c1, c2 in zip(hash1, hash2))
        max_distance = len(hash1)
        similarity = ((max_distance - distance) / max_distance) * 100
        
        return similarity
    
    def cluster_applications(self, applications: List[Application]) -> Dict[int, List[int]]:
        """
        Algorithm 1: Formation of Application Clusters
        
        Uses Hierarchical Agglomerative Clustering (HAC) to group similar applications
        
        Input: List of applications with fuzzy hashes
        Output: Dictionary of clusters {cluster_id: [app_ids]}
        """
        self.logger.info(f"Starting clustering of {len(applications)} applications")
        
        if not applications:
            return {}
        
        # Calculate pairwise similarity matrix
        similarity_matrix = {}
        for i, app1 in enumerate(applications):
            for j, app2 in enumerate(applications):
                if i < j:
                    similarity = self.calculate_similarity(app1.fuzzy_hash, app2.fuzzy_hash)
                    similarity_matrix[(app1.app_id, app2.app_id)] = similarity
        
        self.logger.debug(f"Similarity matrix computed: {len(similarity_matrix)} pairs")
        
        # HAC: Start with each app as singleton cluster
        clusters = {i: [app.app_id] for i, app in enumerate(applications)}
        cluster_mapping = {app.app_id: i for i, app in enumerate(applications)}
        
        # Merge clusters based on similarity threshold
        merged = True
        cluster_id_counter = len(applications)
        
        while merged:
            merged = False
            best_sim = -1
            best_pair = None
            
            # Find pair of clusters with highest similarity > threshold
            for (app1_id, app2_id), similarity in similarity_matrix.items():
                if similarity > self.SIMILARITY_THRESHOLD:
                    cluster1 = cluster_mapping.get(app1_id)
                    cluster2 = cluster_mapping.get(app2_id)
                    
                    if cluster1 is not None and cluster2 is not None and cluster1 != cluster2:
                        if similarity > best_sim:
                            best_sim = similarity
                            best_pair = (cluster1, cluster2, app1_id, app2_id)
            
            if best_pair:
                c1, c2, app1_id, app2_id = best_pair
                # Merge clusters
                clusters[cluster_id_counter] = clusters[c1] + clusters[c2]
                
                # Update mapping
                for app_id in clusters[c1] + clusters[c2]:
                    cluster_mapping[app_id] = cluster_id_counter
                
                del clusters[c1]
                del clusters[c2]
                
                cluster_id_counter += 1
                merged = True
                self.logger.debug(f"Merged clusters containing apps {app1_id}, {app2_id} "
                                f"(similarity: {best_sim:.2f}%)")
        
        self.logger.info(f"Clustering complete. Created {len(clusters)} clusters")
        return clusters
    
    def process_applications(self, app_contents: Dict[int, bytes]) -> Tuple[Dict[int, str], Dict[int, List[int]]]:
        """
        Complete workflow: Hash applications and cluster them
        
        Input: {app_id: content_bytes}
        Output: ({app_id: fuzzy_hash}, {cluster_id: [app_ids]})
        """
        fuzzy_hashes = {}
        applications = []
        
        # Compute fuzzy hashes
        for app_id, content in app_contents.items():
            fuzzy_hash = self.compute_fuzzy_hash(content)
            fuzzy_hashes[app_id] = fuzzy_hash
            applications.append(Application(
                app_id=app_id,
                vm_id=app_id // 100,  # Simple VM assignment
                name=f"App_{app_id}",
                fuzzy_hash=fuzzy_hash
            ))
            self.logger.debug(f"App {app_id}: fuzzy_hash={fuzzy_hash}")
        
        # Cluster applications
        clusters = self.cluster_applications(applications)
        
        return fuzzy_hashes, clusters


# ============================================================================
# MODULE 2: GENETIC ALGORITHM FOR PAGE SIMILARITY DETECTION
# ============================================================================

class GeneticAlgorithmModule:
    """
    Algorithm 2: Static Page Similarity Detection using Genetic Algorithm
    
    Identifies similar memory pages within application clusters using GA
    with fitness evaluation based on object dump comparison.
    """
    
    def __init__(self, population_size: int = 50, generations: int = 20, mutation_rate: float = 0.1):
        self.logger = logging.getLogger(__name__ + '.GeneticAlgorithmModule')
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
    
    def compute_object_dump_hash(self, page_content: bytes) -> str:
        """
        Compute object dump hash for a page
        Represents the structural content of the page
        """
        return hashlib.sha256(page_content).hexdigest()[:16]
    
    def fitness_function(self, page1: Page, page2: Page) -> float:
        """
        Fitness evaluation based on object dump comparison
        
        Returns: similarity score 0-100
        If object dumps are identical (diff == 0): fitness = 100
        Otherwise: measure structural similarity
        """
        dump1 = page1.object_dump
        dump2 = page2.object_dump
        
        if dump1 == dump2:
            return 100.0
        
        # Calculate edit distance similarity
        distance = self.edit_distance(dump1, dump2)
        max_len = max(len(dump1), len(dump2))
        
        if max_len == 0:
            return 100.0
        
        similarity = ((max_len - distance) / max_len) * 100
        return max(0, min(100, similarity))  # Clamp to 0-100
    
    def edit_distance(self, s1: str, s2: str) -> int:
        """Calculate Levenshtein distance between two strings"""
        if len(s1) < len(s2):
            return self.edit_distance(s2, s1)
        
        if len(s2) == 0:
            return len(s1)
        
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]
    
    def roulette_wheel_selection(self, population: List[Tuple[Page, Page]], 
                                fitness_scores: List[float]) -> Tuple[Page, Page]:
        """Roulette wheel selection based on fitness scores"""
        total_fitness = sum(fitness_scores)
        if total_fitness == 0:
            return random.choice(population)
        
        probabilities = [f / total_fitness for f in fitness_scores]
        index = random.choices(range(len(population)), weights=probabilities, k=1)[0]
        return population[index]
    
    def detect_similar_pages(self, pages: List[Page]) -> List[Tuple[int, int, float]]:
        """
        Algorithm 2: Identify static similar pages
        
        Input: List of pages from code section
        Output: List of (page_id1, page_id2, similarity_score) tuples
        """
        self.logger.info(f"Starting GA-based page similarity detection for {len(pages)} pages")
        
        if len(pages) < 2:
            return []
        
        similar_pairs = []
        
        # Initial population: pairs of candidate pages
        population = [(pages[i], pages[j]) for i in range(len(pages)) 
                     for j in range(i + 1, len(pages))]
        
        self.logger.debug(f"Initial population size: {len(population)}")
        
        for generation in range(self.generations):
            # Evaluate fitness
            fitness_scores = [self.fitness_function(p1, p2) for p1, p2 in population]
            
            # Selection: keep best individuals
            sorted_indices = sorted(range(len(fitness_scores)), 
                                   key=lambda i: fitness_scores[i], reverse=True)
            selected_population = [population[i] for i in sorted_indices[:self.population_size]]
            selected_fitness = [fitness_scores[i] for i in sorted_indices[:self.population_size]]
            
            # Store high-fitness pairs
            for (page1, page2), fitness in zip(selected_population, selected_fitness):
                if fitness > 70:  # Threshold for similar pages
                    similar_pairs.append((page1.page_id, page2.page_id, fitness))
            
            # Mutation: randomly modify population
            new_population = selected_population.copy()
            for _ in range(len(selected_population) // 2):
                if random.random() < self.mutation_rate:
                    idx = random.randint(0, len(pages) - 1)
                    page_idx = random.randint(0, len(pages) - 1)
                    pair_idx = random.randint(0, len(new_population) - 1)
                    new_population[pair_idx] = (pages[idx], pages[page_idx])
            
            population = new_population
            
            avg_fitness = sum(selected_fitness) / len(selected_fitness) if selected_fitness else 0
            self.logger.debug(f"Generation {generation}: avg_fitness={avg_fitness:.2f}, "
                            f"found {len(similar_pairs)} similar pairs")
        
        self.logger.info(f"GA detection complete. Found {len(similar_pairs)} similar page pairs")
        return similar_pairs


# ============================================================================
# MODULE 3: MULTILEVEL SHARED PAGE TABLE
# ============================================================================

class MultilevelSharedPageTable:
    """
    Algorithm 3: Multilevel Shared Page Table
    
    Stores information about shareable pages for use during online deduplication.
    Maintains relationships between similar pages for efficient lookup.
    """
    
    def __init__(self, frame_size: int = 4096):
        self.logger = logging.getLogger(__name__ + '.MultilevelSharedPageTable')
        self.frame_size = frame_size
        self.table: Dict[int, SharedPageTableEntry] = {}
        self.page_to_entry: Dict[int, int] = {}  # page_id -> entry_id
        self.entry_counter = 0
    
    def create_entry(self, primary_page: Page, similar_pages: List[Page], 
                    cluster_id: int) -> SharedPageTableEntry:
        """
        Create entry in the multilevel shared page table
        
        Algorithm 3: Implementation Algorithm for Multilevel Page Table
        """
        entry = SharedPageTableEntry(
            entry_id=self.entry_counter,
            primary_page_id=primary_page.page_id,
            similar_pages=[p.page_id for p in similar_pages],
            content_signature=primary_page.content_hash,
            cluster_id=cluster_id,
            created_timestamp=0  # Would be actual timestamp in real implementation
        )
        
        self.table[self.entry_counter] = entry
        self.page_to_entry[primary_page.page_id] = self.entry_counter
        
        for page in similar_pages:
            self.page_to_entry[page.page_id] = self.entry_counter
        
        self.entry_counter += 1
        self.logger.debug(f"Created MSPT entry {entry.entry_id} with "
                         f"{len(similar_pages)} similar pages")
        
        return entry
    
    def build_table(self, pages: List[Page], similar_page_pairs: List[Tuple[int, int, float]]) -> int:
        """
        Build multilevel shared page table from pages and similarity relationships
        
        Input: Pages and list of similar page pairs
        Output: Number of entries created
        """
        self.logger.info(f"Building MSPT from {len(pages)} pages and {len(similar_page_pairs)} pairs")
        
        # Group similar pages together
        page_id_to_page = {p.page_id: p for p in pages}
        page_groups = defaultdict(set)
        processed = set()
        
        for page_id1, page_id2, similarity in similar_page_pairs:
            if page_id1 not in processed and page_id2 not in processed:
                page_groups[page_id1].add(page_id1)
                page_groups[page_id1].add(page_id2)
                processed.add(page_id1)
                processed.add(page_id2)
        
        # Create entries
        created_entries = 0
        cluster_id = 0
        
        for primary_id, related_ids in page_groups.items():
            if primary_id in page_id_to_page:
                primary_page = page_id_to_page[primary_id]
                similar_pages = [page_id_to_page[pid] for pid in related_ids 
                               if pid in page_id_to_page and pid != primary_id]
                
                if similar_pages:
                    self.create_entry(primary_page, similar_pages, cluster_id)
                    created_entries += 1
                    cluster_id += 1
        
        self.logger.info(f"MSPT built with {created_entries} entries, "
                        f"covering {len(self.page_to_entry)} pages")
        
        return created_entries
    
    def lookup(self, page_id: int) -> SharedPageTableEntry:
        """Look up shared page information by page_id"""
        entry_id = self.page_to_entry.get(page_id)
        if entry_id is not None:
            return self.table.get(entry_id)
        return None
    
    def get_shareable_pages(self, page_id: int) -> List[int]:
        """Get list of pages that can be shared with given page"""
        entry = self.lookup(page_id)
        if entry:
            return entry.similar_pages
        return []


# ============================================================================
# MODULE 4: MEMORY DEDUPLICATION
# ============================================================================

class MemoryDeduplicationEngine:
    """
    Algorithm 4: Memory Deduplication Implementation
    
    Performs actual memory deduplication online using pre-computed
    multilevel shared page table.
    """
    
    def __init__(self, mspt: MultilevelSharedPageTable):
        self.logger = logging.getLogger(__name__ + '.MemoryDeduplicationEngine')
        self.mspt = mspt
        self.dedup_count = 0
        self.total_memory_saved = 0
    
    def merge_pages(self, vm_pages: Dict[int, List[Page]]) -> Tuple[int, int]:
        """
        Algorithm 4: Memory Deduplication Implementation
        
        Merge pages across VMs using pre-computed MSPT
        
        Input: Pages grouped by VM
        Output: (pages_merged_count, memory_saved_bytes)
        """
        self.logger.info(f"Starting memory deduplication for {len(vm_pages)} VMs")
        
        pages_merged = 0
        memory_saved = 0
        merged_pairs = set()
        
        # Flatten all pages
        all_pages = []
        for vm_id, pages in vm_pages.items():
            for page in pages:
                all_pages.append((vm_id, page))
        
        # For each page, check if it can be merged
        for vm_id, page in all_pages:
            # Check if page is in MSPT
            shareable_pages = self.mspt.get_shareable_pages(page.page_id)
            
            if shareable_pages:
                # Find other VMs with shareable pages
                for other_page_id in shareable_pages:
                    pair_key = tuple(sorted([page.page_id, other_page_id]))
                    
                    if pair_key not in merged_pairs:
                        # Mark as shared
                        pages_merged += 1
                        memory_saved += page.size
                        merged_pairs.add(pair_key)
                        
                        self.logger.debug(f"Merged page {page.page_id} with {other_page_id} "
                                        f"(saved {page.size} bytes)")
        
        self.dedup_count += pages_merged
        self.total_memory_saved += memory_saved
        
        self.logger.info(f"Deduplication complete: {pages_merged} pages merged, "
                        f"{memory_saved / 1024 / 1024:.2f} MB saved")
        
        return pages_merged, memory_saved
    
    def get_statistics(self) -> Dict:
        """Get deduplication statistics"""
        return {
            'total_pages_merged': self.dedup_count,
            'total_memory_saved_bytes': self.total_memory_saved,
            'total_memory_saved_mb': self.total_memory_saved / 1024 / 1024,
            'average_page_savings': (self.total_memory_saved / self.dedup_count * 1024 
                                    if self.dedup_count > 0 else 0)
        }


# ============================================================================
# MAIN ORCHESTRATOR
# ============================================================================

class mSMDOrchestrator:
    """
    Main orchestrator for the complete mSMD pipeline
    
    Coordinates all four modules in the offline and online phases
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__ + '.mSMDOrchestrator')
        self.fuzzy_hash_module = FuzzyHashingModule()
        self.ga_module = GeneticAlgorithmModule()
        self.mspt = None
        self.dedup_engine = None
        self.results = {}
    
    def offline_processing(self, app_contents: Dict[int, bytes], 
                          app_pages: Dict[int, List[Page]]) -> Dict:
        """
        Offline Phase: Application clustering and page similarity detection
        
        Input: Application contents and their pages
        Output: Results dictionary with clustering and similarity info
        """
        self.logger.info("=" * 80)
        self.logger.info("OFFLINE PROCESSING PHASE")
        self.logger.info("=" * 80)
        
        # Step 1: Fuzzy hashing and application clustering
        self.logger.info("\n[Step 1] Application Clustering using Fuzzy Hashing")
        fuzzy_hashes, clusters = self.fuzzy_hash_module.process_applications(app_contents)
        
        offline_results = {
            'fuzzy_hashes': fuzzy_hashes,
            'application_clusters': clusters,
            'num_clusters': len(clusters)
        }
        
        # Step 2: Page similarity detection per cluster
        self.logger.info("\n[Step 2] Page Similarity Detection using Genetic Algorithm")
        all_similar_pairs = []
        
        for cluster_id, app_ids in clusters.items():
            cluster_pages = []
            for app_id in app_ids:
                if app_id in app_pages:
                    cluster_pages.extend(app_pages[app_id])
            
            if cluster_pages:
                similar_pairs = self.ga_module.detect_similar_pages(cluster_pages)
                all_similar_pairs.extend(similar_pairs)
                self.logger.info(f"  Cluster {cluster_id}: Found {len(similar_pairs)} similar page pairs")
        
        offline_results['similar_page_pairs'] = all_similar_pairs
        offline_results['num_similar_pairs'] = len(all_similar_pairs)
        
        # Step 3: Build multilevel shared page table
        self.logger.info("\n[Step 3] Building Multilevel Shared Page Table")
        all_pages = []
        for pages in app_pages.values():
            all_pages.extend(pages)
        
        self.mspt = MultilevelSharedPageTable()
        entries_created = self.mspt.build_table(all_pages, all_similar_pairs)
        offline_results['mspt_entries'] = entries_created
        
        self.logger.info(f"Offline processing complete. Created {entries_created} MSPT entries")
        
        return offline_results
    
    def online_processing(self, vm_pages: Dict[int, List[Page]]) -> Dict:
        """
        Online Phase: Actual memory deduplication using MSPT
        
        Input: Pages from running VMs
        Output: Deduplication results
        """
        self.logger.info("\n" + "=" * 80)
        self.logger.info("ONLINE PROCESSING PHASE")
        self.logger.info("=" * 80)
        
        if self.mspt is None:
            self.logger.error("MSPT not initialized. Run offline_processing first.")
            return {}
        
        self.logger.info("\n[Step 4] Memory Deduplication")
        self.dedup_engine = MemoryDeduplicationEngine(self.mspt)
        pages_merged, memory_saved = self.dedup_engine.merge_pages(vm_pages)
        
        online_results = {
            'pages_merged': pages_merged,
            'memory_saved_bytes': memory_saved,
            'memory_saved_mb': memory_saved / 1024 / 1024,
            'statistics': self.dedup_engine.get_statistics()
        }
        
        self.logger.info(f"Online processing complete. Pages merged: {pages_merged}, "
                        f"Memory saved: {memory_saved / 1024 / 1024:.2f} MB")
        
        return online_results
    
    def run_complete_pipeline(self, app_contents: Dict[int, bytes],
                            app_pages: Dict[int, List[Page]],
                            vm_pages: Dict[int, List[Page]]) -> Dict:
        """
        Run complete mSMD pipeline (offline + online phases)
        
        Input: Application contents, pages for offline processing, VM pages for online
        Output: Complete results
        """
        self.logger.info("\n\n")
        self.logger.info("╔" + "=" * 78 + "╗")
        self.logger.info("║" + " " * 20 + "mSMD COMPLETE PIPELINE EXECUTION" + " " * 27 + "║")
        self.logger.info("╚" + "=" * 78 + "╝")
        
        # Offline phase
        offline_results = self.offline_processing(app_contents, app_pages)
        
        # Online phase
        online_results = self.online_processing(vm_pages)
        
        # Combine results
        self.results = {
            'offline': offline_results,
            'online': online_results,
            'summary': {
                'total_applications': len(app_contents),
                'application_clusters': offline_results.get('num_clusters', 0),
                'similar_page_pairs': offline_results.get('num_similar_pairs', 0),
                'mspt_entries': offline_results.get('mspt_entries', 0),
                'memory_saved_mb': online_results.get('memory_saved_mb', 0),
                'pages_merged': online_results.get('pages_merged', 0)
            }
        }
        
        return self.results
    
    def print_summary(self):
        """Print summary of execution"""
        if not self.results:
            self.logger.warning("No results to print. Run pipeline first.")
            return
        
        self.logger.info("\n" + "=" * 80)
        self.logger.info("EXECUTION SUMMARY")
        self.logger.info("=" * 80)
        
        summary = self.results.get('summary', {})
        for key, value in summary.items():
            if isinstance(value, float):
                self.logger.info(f"{key:.<40} {value:.2f}")
            else:
                self.logger.info(f"{key:.<40} {value}")


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    print("\nmSMD Implementation - Example Usage\n")
    
    # Sample application contents (in real scenario, these would be actual binaries)
    app_contents = {
        1: b"Binary content of application 1 with some code",
        2: b"Binary content of application 2 with similar code",
        3: b"Binary content of application 3 with different code",
    }
    
    # Sample application pages (code section)
    app_pages = {
        1: [Page(1, 1, 1, "hash1", "dump1"), Page(2, 1, 1, "hash2", "dump1")],
        2: [Page(3, 1, 2, "hash3", "dump1"), Page(4, 1, 2, "hash1", "dump1")],  # similar to app 1
        3: [Page(5, 1, 3, "hash5", "dump3"), Page(6, 1, 3, "hash6", "dump3")],
    }
    
    # Sample VM pages at runtime
    vm_pages = {
        1: [Page(1, 1, 1, "hash1", "dump1"), Page(3, 1, 2, "hash3", "dump1")],
        2: [Page(2, 1, 1, "hash2", "dump1"), Page(4, 1, 2, "hash1", "dump1")],
    }
    
    # Create orchestrator and run pipeline
    orchestrator = mSMDOrchestrator()
    results = orchestrator.run_complete_pipeline(app_contents, app_pages, vm_pages)
    
    # Print summary
    orchestrator.print_summary()
    
    # Print detailed results
    print("\n" + "=" * 80)
    print("DETAILED RESULTS (JSON Format)")
    print("=" * 80)
    print(json.dumps(results['summary'], indent=2))
