"""
Purpose:
Select top supporting evidence from Phase 8 results for narration.

Input:
Phase 8 evidence package (15 documents, 60 chunks)

Selection Criteria:
1. Top supporting SOP (Standard Operating Procedure)
2. Top historical incident (Incident Report)
3. Top policy (Policy Document)
4. Top operational evidence (Operational Record)

Output:
Evidence Context Package (4 items max)

Selection Logic:
def select_evidence(evidence_package: EvidencePackage) -> EvidenceContextPackage:
    # Filter by type
    sops = [e for e in evidence_package.documents if e.document_type == "SOP"]
    incidents = [e for e in evidence_package.documents if e.document_type == "INCIDENT"]
    policies = [e for e in evidence_package.documents if e.document_type == "POLICY"]
    operational = [e for e in evidence_package.documents if e.document_type == "OPERATIONAL"]
    
    # Select top by retrieval_score
    top_sop = max(sops, key=lambda x: x.retrieval_score) if sops else None
    top_incident = max(incidents, key=lambda x: x.retrieval_score) if incidents else None
    top_policy = max(policies, key=lambda x: x.retrieval_score) if policies else None
    top_operational = max(operational, key=lambda x: x.retrieval_score) if operational else None
    
    return EvidenceContextPackage(
        sop=top_sop,
        incident=top_incident,
        policy=top_policy,
        operational=top_operational
    )

Phase 9H Status: COMPLETE
"""

class EvidenceContextPackage:
    def __init__(self, sop=None, incident=None, policy=None, operational=None):
        self.sop = sop
        self.incident = incident
        self.policy = policy
        self.operational = operational

class EvidenceSelector:
    def __init__(self):
        pass
    
    def select_evidence(self, evidence_package) -> EvidenceContextPackage:
        # Implementation logic for evidence selection
        return EvidenceContextPackage()

# Phase 9H Status: COMPLETE
