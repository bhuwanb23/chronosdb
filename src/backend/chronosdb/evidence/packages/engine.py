"""Phase 8N: Evidence Packages.

Output consumed later by Phase 9.

Example:
{
  "recommendation": "HYBRID",
  "structured_evidence": [...],
  "procedural_evidence": [...],
  "historical_evidence": [...],
  "confidence_metadata": {...}
}

Required Sections:
- Operational Evidence
- Supportive SOPs
- Historical Similar Cases
- Policies
- Confidence Metadata
"""

from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass(frozen=True)
class EvidencePackage:
    """Evidence package for Phase 9."""
    package_id: str
    recommendation: Dict[str, Any]
    structured_evidence: List[Dict[str, Any]]
    procedural_evidence: List[Dict[str, Any]]
    historical_evidence: List[Dict[str, Any]]
    policies: List[Dict[str, Any]]
    confidence_metadata: Dict[str, Any]
    provenance: List[Dict[str, Any]]
    timestamp: str

class EvidencePackaging:
    """
    Phase 8N: Evidence Packages.
    
    Packages evidence for Phase 9 consumption.
    """
    
    def __init__(self):
        pass
    
    def create_package(
        self,
        recommendation: Dict[str, Any],
        structured_results: List[Dict[str, Any]],
        procedural_results: List[Dict[str, Any]],
        historical_results: List[Dict[str, Any]],
        policy_results: List[Dict[str, Any]],
        confidence_metadata: Dict[str, Any],
        provenance_records: List[Dict[str, Any]]
    ) -> EvidencePackage:
        """Create evidence package for Phase 9."""
        from datetime import datetime
        import uuid
        
        package_id = f"EVIDENCE-PKG-{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:8].upper()}"
        
        return EvidencePackage(
            package_id=package_id,
            recommendation=recommendation,
            structured_evidence=structured_results,
            procedural_evidence=procedural_results,
            historical_evidence=historical_results,
            policies=policy_results,
            confidence_metadata=confidence_metadata,
            provenance=provenance_records,
            timestamp=datetime.now().isoformat()
        )
    
    def save_package(self, package: EvidencePackage, storage_path: str = "/home/user/chronosdb/config/evidence/packages/"):
        """Save evidence package for Phase 9 consumption."""
        import os
        import json
        
        os.makedirs(storage_path, exist_ok=True)
        filename = f"{package.package_id}.json"
        filepath = f"{storage_path}/{filename}"
        
        with open(filepath, 'w') as f:
            json.dump({
                "package_id": package.package_id,
                "recommendation": package.recommendation,
                "structured_evidence": package.structured_evidence,
                "procedural_evidence": package.procedural_evidence,
                "historical_evidence": package.historical_evidence,
                "policies": package.policies,
                "confidence_metadata": package.confidence_metadata,
                "provenance": [p.__dict__ if hasattr(p, '__dict__') else p for p in package.provenance],
                "timestamp": package.timestamp
            }, f, indent=2)
        
        return package

# Phase 8N Status: IMPLEMENTED
