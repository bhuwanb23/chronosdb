"""Phase 7Q: Performance.

Operation Targets (p95):
- Feasibility: <100 ms
- Utility Calculation: <100 ms
- Pareto Construction: <200 ms
- Optimization: <500 ms
- Sensitivity Analysis: <2 sec
"""

import time
from typing import List, Dict, Any, Callable
from dataclasses import dataclass

@dataclass(frozen=True)
class PerformanceResult:
    """Performance evaluation result."""
    operation: str
    execution_time_ms: float
    target_time_ms: float
    passed: bool
    p95_estimate: float
    analysis_details: Dict[str, Any]

class PerformanceEvaluation:
    """
    Phase 7Q: Performance Evaluation.
    
    Evaluates optimization performance against targets.
    """
    
    def __init__(self):
        # Performance targets (p95 in milliseconds)
        self.targets = {
            "feasibility": 100,
            "utility_calculation": 100,
            "pareto_construction": 200,
            "optimization": 500,
            "sensitivity_analysis": 2000  # 2 seconds
        }
    
    def measure_execution_time(self, operation: Callable, *args, **kwargs) -> float:
        """Measure execution time in milliseconds."""
        start_time = time.time()
        operation(*args, **kwargs)
        end_time = time.time()
        return (end_time - start_time) * 1000  # Convert to milliseconds
    
    def evaluate_performance(
        self,
        operation_name: str,
        operation_func: Callable,
        operation_args: tuple = (),
        operation_kwargs: dict = None,
        iterations: int = 10
    ) -> PerformanceResult:
        """
        Evaluate performance of an operation.
        
        Runs operation multiple times to estimate p95.
        """
        if operation_kwargs is None:
            operation_kwargs = {}
        
        execution_times = []
        
        # Run multiple iterations to estimate p95
        for _ in range(iterations):
            execution_time = self.measure_execution_time(
                operation_func, *operation_args, **operation_kwargs
            )
            execution_times.append(execution_time)
        
        # Calculate p95 (95th percentile)
        execution_times.sort()
        p95_index = int(len(execution_times) * 0.95)
        p95_time = execution_times[p95_index] if p95_index < len(execution_times) else execution_times[-1]
        
        # Get target time
        target_time = self.targets.get(operation_name, 1000)  # Default 1s
        
        # Check if passed
        passed = p95_time <= target_time
        
        # Calculate average time
        avg_time = sum(execution_times) / len(execution_times)
        
        return PerformanceResult(
            operation=operation_name,
            execution_time_ms=avg_time,
            target_time_ms=target_time,
            passed=passed,
            p95_estimate=p95_time,
            analysis_details={
                "iterations": iterations,
                "execution_times": execution_times,
                "min_time": min(execution_times),
                "max_time": max(execution_times),
                "avg_time": avg_time,
                "p95_time": p95_time,
                "target_time": target_time,
                "passed": passed
            }
        )
    
    def evaluate_all_operations(
        self,
        feasibility_func, feasibility_args,
        utility_func, utility_args,
        pareto_func, pareto_args,
        optimization_func, optimization_args,
        sensitivity_func, sensitivity_args,
        iterations: int = 10
    ) -> List[PerformanceResult]:
        """Evaluate performance of all optimization operations."""
        results = []
        
        # Feasibility
        results.append(self.evaluate_performance(
            "feasibility", feasibility_func, feasibility_args, {}, iterations
        ))
        
        # Utility calculation
        results.append(self.evaluate_performance(
            "utility_calculation", utility_func, utility_args, {}, iterations
        ))
        
        # Pareto construction
        results.append(self.evaluate_performance(
            "pareto_construction", pareto_func, pareto_args, {}, iterations
        ))
        
        # Optimization
        results.append(self.evaluate_performance(
            "optimization", optimization_func, optimization_args, {}, iterations
        ))
        
        # Sensitivity analysis
        results.append(self.evaluate_performance(
            "sensitivity_analysis", sensitivity_func, sensitivity_args, {}, iterations
        ))
        
        return results

# Phase 7Q Status: IMPLEMENTED
