import React, { useState } from 'react';
import { ExecutiveDashboard } from './components/executive/ExecutiveDashboard';
import { DependencyCascadeVisualization } from './components/cascade/DependencyCascadeVisualization';
import { InterventionComparisonCenter } from './components/interventions/InterventionComparisonCenter';
import { TimelineAndDecisionReplay } from './components/replay/TimelineAndDecisionReplay';
import { EvidenceExplorer } from './components/evidence/EvidenceExplorer';
import { AuditExplorer } from './components/audit/AuditExplorer';
import { NaturalLanguageConsole } from './components/ai-console/NaturalLanguageConsole';
import { JudgeDemoMode } from './components/demo/JudgeDemoMode';

const App: React.FC = () => {
  const [isDemoRunning, setIsDemoRunning] = useState(false);

  const nodes = [
    { id: 'SUP-0104', label: 'SUP-0104', type: 'supplier' as const, status: 'critical' as const },
    { id: 'CMP-MCU-42', label: 'CMP-MCU-42', type: 'component' as const, status: 'warning' as const },
    { id: 'MO-0882', label: 'MO-0882', type: 'order' as const, status: 'warning' as const },
    { id: 'CO-0704', label: 'CO-0704', type: 'order' as const, status: 'critical' as const },
    { id: 'REV', label: 'Revenue Risk', type: 'revenue' as const, status: 'critical' as const },
  ];

  const links = [
    { source: 'SUP-0104', target: 'CMP-MCU-42' },
    { source: 'CMP-MCU-42', target: 'MO-0882' },
    { source: 'MO-0882', target: 'CO-0704' },
    { source: 'CO-0704', target: 'REV' },
  ];

  const interventions = [
    { type: 'DO_NOTHING', cost: 0, delay: 720, revenueProtected: 0, breachesAvoided: 0, utilityScore: 0.1, isRecommended: false },
    { type: 'TRANSFER', cost: 50000, delay: 240, revenueProtected: 800000, breachesAvoided: 1, utilityScore: 0.6, isRecommended: false },
    { type: 'HYBRID', cost: 132000, delay: 120, revenueProtected: 1200000, breachesAvoided: 2, utilityScore: 0.91, isRecommended: true },
  ];

  const stages = [
    { stage: 'Healthy State', timestamp: 'T0', facts: ['All systems normal'], evidence: [], decisionState: 'HEALTHY' },
    { stage: 'Disruption Detected', timestamp: 'T1', facts: ['Supplier outage'], evidence: [], decisionState: 'DISRUPTED' },
    { stage: 'Impact Computed', timestamp: 'T2', facts: ['Revenue at risk'], evidence: [], decisionState: 'IMPACTED' },
    { stage: 'Simulation Executed', timestamp: 'T3', facts: ['Scenarios run'], evidence: [], decisionState: 'SIMULATED' },
    { stage: 'Optimization Completed', timestamp: 'T4', facts: ['HYBRID selected'], evidence: [], decisionState: 'OPTIMIZED' },
    { stage: 'Recommendation Generated', timestamp: 'T5', facts: ['Recommendation ready'], evidence: [], decisionState: 'RECOMMENDED' },
  ];

  const evidenceItems = [
    { id: 'E1', title: 'Warehouse Transfer SOP', type: 'sop' as const, version: '1.0', score: 0.92, source: 'DOC-104' },
  ];

  const auditRecords = [
    {
      decisionId: 'D-882',
      correlationId: 'CID-001',
      scenario: 'SCN-001',
      simulation: 'SIM-001',
      recommendation: 'HYBRID',
      verificationStatus: 'VERIFIED',
      replayHistory: ['REPLAY-001'],
      timestamp: '2026-11-14T00:00:00Z',
    },
  ];

  return (
    <div className="chronosdb-war-room">
      <JudgeDemoMode onDemoStart={() => setIsDemoRunning(true)} onDemoComplete={() => setIsDemoRunning(false)} />
      <ExecutiveDashboard
        revenueAtRisk={1600000}
        slaBreaches={2}
        affectedOrders={10}
        activeDisruptions={1}
        recoverySavings={1100000}
        recommendationConfidence={91}
      />
      <DependencyCascadeVisualization nodes={nodes} links={links} />
      <InterventionComparisonCenter interventions={interventions} />
      <TimelineAndDecisionReplay stages={stages} onStageChange={() => {}} />
      <EvidenceExplorer evidenceItems={evidenceItems} />
      <AuditExplorer auditRecords={auditRecords} />
      <NaturalLanguageConsole onQuerySubmit={() => {}} />
    </div>
  );
};

export default App;
