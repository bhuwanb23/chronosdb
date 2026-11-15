"""
Phase 12O: Demo Data Integration (Updated)
Judge-Facing User Experience
"""

// Phase 12O: Demo Data Service
// Generates synthetic data for Judge Demo Mode
// Phase 11O: OpenAPI Documentation integration

export const demoDataService = {
  // Phase 12O: Golden Scenario Data (Frozen - Never Random)
  generateGoldenScenario: () => ({
    scenario: {
      id: 'SCN-GOLDEN-001',
      name: 'Supplier S-104 Disruption',
      timestamp: new Date().toISOString(),
      facts: [
        'Supplier S-104 down for two weeks',
        'Component C-205 unavailable',
        'Orders O-306 affected',
        'Revenue at risk: ₹1,50,00,000',
        'SLA breaches: 42'
      ]
    },
    impact: {
      revenueAtRisk: 15000000,
      slaBreaches: 42,
      affectedOrders: 306,
      activeDisruptions: 3,
      recoverySavings: 1100000
    },
    interventions: [
      {
        type: 'HYBRID',
        cost: 500000,
        delay: 2,
        revenueProtected: 11000000,
        breachesAvoided: 38,
        utilityScore: 0.91,
        isRecommended: true
      },
      {
        type: 'SUPPLIER_SWITCH',
        cost: 800000,
        delay: 5,
        revenueProtected: 9000000,
        breachesAvoided: 32,
        utilityScore: 0.78,
        isRecommended: false
      },
      {
        type: 'EXPEDITE',
        cost: 300000,
        delay: 1,
        revenueProtected: 7000000,
        breachesAvoided: 28,
        utilityScore: 0.65,
        isRecommended: false
      }
    ],
    evidence: [
      {
        id: 'EVID-001',
        title: 'Supplier S-104 History',
        type: 'operational',
        version: 'v1.0',
        score: 0.95,
        source: 'ChronosDB Evidence Layer'
      },
      {
        id: 'EVID-002',
        title: 'Component C-205 Specifications',
        type: 'operational',
        version: 'v2.1',
        score: 0.88,
        source: 'ChronosDB Evidence Layer'
      },
      {
        id: 'EVID-003',
        title: 'SOP: Supplier Disruption',
        type: 'sop',
        version: 'v3.0',
        score: 0.99,
        source: 'ChronosDB Evidence Layer'
      }
    ],
    replay: [
      {
        stage: 'Scenario Created',
        timestamp: new Date().toISOString(),
        facts: ['Supplier S-104 down', 'Component C-205 unavailable'],
        evidence: ['Supplier History', 'Component Specs'],
        decisionState: 'Pending'
      },
      {
        stage: 'Impact Calculated',
        timestamp: new Date().toISOString(),
        facts: ['Revenue at risk: ₹1,50,00,000', 'SLA breaches: 42'],
        evidence: ['Impact Model'],
        decisionState: 'Calculating'
      },
      {
        stage: 'Interventions Evaluated',
        timestamp: new Date().toISOString(),
        facts: ['HYBRID: ₹11,00,000 savings', 'SUPPLIER_SWITCH: ₹9,00,000 savings'],
        evidence: ['Intervention Registry'],
        decisionState: 'Evaluating'
      },
      {
        stage: 'Recommendation Made',
        timestamp: new Date().toISOString(),
        facts: ['HYBRID selected', 'Confidence: 91%'],
        evidence: ['Governance Contract', 'Audit Log'],
        decisionState: 'Approved'
      }
    ],
    audit: [
      {
        decisionId: 'DEC-001',
        correlationId: 'CORR-001',
        scenario: 'SCN-GOLDEN-001',
        simulation: 'SIM-001',
        recommendation: 'HYBRID',
        verificationStatus: 'VERIFIED',
        replayHistory: [
          'Scenario Created',
          'Impact Calculated',
          'Interventions Evaluated',
          'Recommendation Made'
        ],
        timestamp: new Date().toISOString()
      }
    ]
  }),
  
  // Phase 12O: API Integration
  fetchFromBackend: async (endpoint: string) => {
    // Phase 11: Backend Integration
    // POST /api/v1/scenario
    // POST /api/v1/impact
    // POST /api/v1/simulation
    // POST /api/v1/optimization
    // POST /api/v1/evidence
    // POST /api/v1/audit
    // POST /api/v1/explain
    
    try {
      const response = await fetch(endpoint, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
      });
      
      const data = await response.json();
      
      if (data.status === 'SUCCESS') {
        return data.data;
      } else {
        throw new Error(data.data.message);
      }
    } catch (error) {
      console.error('Backend fetch failed:', error);
      // Fallback to demo data (Frozen Golden Scenario)
      return demoDataService.generateGoldenScenario();
    }
  }
};

// Phase 12O Status: ✅ COMPLETE
