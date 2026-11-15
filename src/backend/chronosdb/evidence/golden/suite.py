"""Phase 8P: Golden Retrieval Suite.

Locked Retrieval Questions:
Question 1: Show procedures supporting warehouse transfer.
Expected: Transfer SOP

Question 2: Show similar supplier outages.
Expected: Historical Incident Documents

Question 3: Show supplier substitution guidance.
Expected: Approved Supplier Rules

Golden Requirement:
Top retrieved evidence must match frozen expectations.
"""

from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass(frozen=True)
class GoldenRetrievalScenario:
    """Golden retrieval scenario."""
    scenario_id: str
    description: str
    query: str
    expected_evidence: List[Dict[str, Any]]
    expected_scores: Dict[str, float]
    golden_requirement: str
    metadata: Dict[str, Any]

class GoldenRetrievalSuite:
    """
    Phase 8P: Golden Retrieval Suite.
    
    Provides standard golden retrieval scenarios for benchmarking.
    """
    
    def __init__(self):
        self.scenarios = self._load_scenarios()
    
    def _load_scenarios(self) -> List[GoldenRetrievalScenario]:
        """Load standard golden retrieval scenarios."""
        
        # Scenario 1: Warehouse Transfer Procedure
        scenario1 = GoldenRetrievalScenario(
            scenario_id="GOLD-RETRIEVAL-001",
            description="Show procedures supporting warehouse transfer",
            query="warehouse transfer procedure for MCU components",
            expected_evidence=[
                {
                    "document_id": "DOC-104",
                    "chunk_id": "CH-104-001",
                    "type": "PROCEDURAL",
                    "source_document": "Warehouse Recovery SOP",
                    "version": "1.2",
                    "expected_score": 0.92
                }
            ],
            expected_scores={
                "recall@5": 0.85,
                "precision@5": 0.80,
                "mrr": 0.80,
                "metadata_accuracy": 1.0,
                "unsupported_sources": 0.0
            },
            golden_requirement="Top retrieved evidence must match Transfer SOP",
            metadata={
                "region": "INDIA",
                "effective_from": "2026-01-01",
                "document_type": "PROCEDURAL"
            }
        )
        
        # Scenario 2: Similar supplier outages
        scenario2 = GoldenRetrievalScenario(
            scenario_id="GOLD-RETRIEVAL-002",
            description="Show similar supplier outages",
            query="supplier outage delaying MCU delivery",
            expected_evidence=[
                {
                    "document_id": "DOC-205",
                    "chunk_id": "CH-205-003",
                    "type": "HISTORICAL",
                    "source_document": "Incident Report 2025-SUP-0104",
                    "version": "1.0",
                    "expected_score": 0.85
                }
            ],
            expected_scores={
                "recall@5": 0.85,
                "precision@5": 0.80,
                "mrr": 0.80,
                "metadata_accuracy": 1.0,
                "unsupported_sources": 0.0
            },
            golden_requirement="Top retrieved evidence must match Historical Incident Documents",
            metadata={
                "region": "INDIA",
                "effective_from": "2025-06-15",
                "document_type": "HISTORICAL"
            }
        )
        
        # Scenario 3: Supplier substitution guidance
        scenario3 = GoldenRetrievalScenario(
            scenario_id="GOLD-RETRIEVAL-003",
            description="Show supplier substitution guidance",
            query="supplier substitution guidance for MCU-42",
            expected_evidence=[
                {
                    "document_id": "DOC-306",
                    "chunk_id": "CH-306-002",
                    "type": "GOVERNANCE",
                    "source_document": "Approved Supplier Rules",
                    "version": "2.0",
                    "expected_score": 0.78
                }
            ],
            expected_scores={
                "recall@5": 0.85,
                "precision@5": 0.80,
                "mrr": 0.80,
                "metadata_accuracy": 1.0,
                "unsupported_sources": 0.0
            },
            golden_requirement="Top retrieved evidence must match Approved Supplier Rules",
            metadata={
                "region": "INDIA",
                "effective_from": "2026-01-01",
                "document_type": "GOVERNANCE"
            }
        )
        
        return [scenario1, scenario2, scenario3]
    
    def get_scenario(self, scenario_id: str) -> GoldenRetrievalScenario:
        """Get specific golden scenario."""
        for scenario in self.scenarios:
            if scenario.scenario_id == scenario_id:
                return scenario
        raise ValueError(f"Golden retrieval scenario {scenario_id} not found")
    
    def list_scenarios(self) -> List[GoldenRetrievalScenario]:
        """List all golden retrieval scenarios."""
        return self.scenarios

# Phase 8P Status: IMPLEMENTED
