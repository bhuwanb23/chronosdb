"""Phase 8T: Retrieval Performance.

Performance Targets:
- Structured retrieval: P95 < 50ms
- Semantic retrieval: P95 < 100ms
- Hybrid combination: P95 < 150ms
- Ranking classification: P95 < 20ms
- Package creation: P95 < 30ms
- Overall end-to-end: P95 < 350ms

Metrics:
- Latency (P95)
- Throughput (queries/sec)
- Memory usage
- CPU usage
"""

from dataclasses import dataclass
from typing import List, Dict, Any
import time

@dataclass(frozen=True)
class PerformanceResult:
    """Retrieval performance result."""
    metric_id: str
    operation: str
    p95_latency_ms: float
    throughput_qps: float
    memory_usage_mb: float
    cpu_usage_percent: float
    target_met: bool
    analysis: Dict[str, Any]

class RetrievalPerformance:
    """
    Phase 8T: Retrieval Performance.
    
    Evaluates and monitors retrieval performance metrics.
    """
    
    def __init__(self):
        # Performance targets (P95)
        self.targets = {
            "structured_retrieval": 50.0,
            "semantic_retrieval": 100.0,
            "hybrid_combination": 150.0,
            "ranking_classification": 20.0,
            "package_creation": 30.0,
            "overall_end_to_end": 350.0
        }
    
    def measure_performance(
        self,
        operation: str,
        execution_times: List[float],
        throughput_data: Dict[str, Any],
        resource_usage: Dict[str, Any]
    ) -> PerformanceResult:
        """Measure performance for specific operation."""
        
        # Calculate P95 latency
        p95_latency = self._calculate_p95(execution_times)
        
        # Calculate throughput (queries per second)
        throughput_qps = throughput_data.get("queries_per_second", 0.0)
        
        # Extract resource usage
        memory_usage = resource_usage.get("memory_mb", 0.0)
        cpu_usage = resource_usage.get("cpu_percent", 0.0)
        
        # Check target
        target = self.targets.get(operation, 1000.0)
        target_met = p95_latency <= target
        
        return PerformanceResult(
            metric_id=f"PERF-{operation.upper()}",
            operation=operation,
            p95_latency_ms=p95_latency,
            throughput_qps=throughput_qps,
            memory_usage_mb=memory_usage,
            cpu_usage_percent=cpu_usage,
            target_met=target_met,
            analysis={
                "target": target,
                "actual": p95_latency,
                "difference": target - p95_latency,
                "status": "PASSED" if target_met else "FAILED"
            }
        )
    
    def _calculate_p95(self, execution_times: List[float]) -> float:
        """Calculate P95 latency."""
        if not execution_times:
            return 0.0
        
        # Sort and find 95th percentile
        sorted_times = sorted(execution_times)
        index = int(len(sorted_times) * 0.95)
        return sorted_times[min(index, len(sorted_times) - 1)]
    
    def run_performance_suite(
        self,
        structured_times: List[float],
        semantic_times: List[float],
        hybrid_times: List[float],
        ranking_times: List[float],
        package_times: List[float],
        overall_times: List[float],
        throughput_data: Dict[str, Any],
        resource_usage: Dict[str, Any]
    ) -> List[PerformanceResult]:
        """Run complete performance suite."""
        results = []
        
        # Structured retrieval
        results.append(self.measure_performance(
            "structured_retrieval", structured_times, throughput_data, resource_usage
        ))
        
        # Semantic retrieval
        results.append(self.measure_performance(
            "semantic_retrieval", semantic_times, throughput_data, resource_usage
        ))
        
        # Hybrid combination
        results.append(self.measure_performance(
            "hybrid_combination", hybrid_times, throughput_data, resource_usage
        ))
        
        # Ranking classification
        results.append(self.measure_performance(
            "ranking_classification", ranking_times, throughput_data, resource_usage
        ))
        
        # Package creation
        results.append(self.measure_performance(
            "package_creation", package_times, throughput_data, resource_usage
        ))
        
        # Overall end-to-end
        results.append(self.measure_performance(
            "overall_end_to_end", overall_times, throughput_data, resource_usage
        ))
        
        return results

# Phase 8T Status: IMPLEMENTED
