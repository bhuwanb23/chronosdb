import React from 'react';
import { Card, Typography, Grid, Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from '@mui/material';

interface AuditRecord {
  decisionId: string;
  correlationId: string;
  scenario: string;
  simulation: string;
  recommendation: string;
  verificationStatus: string;
  replayHistory: string[];
  timestamp: string;
}

interface AuditExplorerProps {
  auditRecords: AuditRecord[];
}

export const AuditExplorer: React.FC<AuditExplorerProps> = ({
  auditRecords
}) => {
  return (
    <div className="audit-explorer">
      <Typography variant="h5">Audit Explorer</Typography>
      <Typography variant="body2">Enterprise differentiator: Audit as story, not table</Typography>
      
      <TableContainer>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Decision ID</TableCell>
              <TableCell>Correlation ID</TableCell>
              <TableCell>Scenario</TableCell>
              <TableCell>Recommendation</TableCell>
              <TableCell>Verification</TableCell>
              <TableCell>Audit Time</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {auditRecords.map((audit, index) => (
              <TableRow key={index}>
                <TableCell>{audit.decisionId}</TableCell>
                <TableCell>{audit.correlationId}</TableCell>
                <TableCell>{audit.scenario}</TableCell>
                <TableCell>{audit.recommendation}</TableCell>
                <TableCell>{audit.verificationStatus}</TableCell>
                <TableCell>{audit.timestamp}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
      
      {/* Replay History */}
      <Card className="replay-history">
        <Typography variant="h6">Replay History</Typography>
        <div>
          {auditRecords.flatMap(audit => audit.replayHistory).map((replay, index) => (
            <Typography key={index} variant="body2">{replay}</Typography>
          ))}
        </div>
      </Card>
    </div>
  );
};

// Phase 12I Status: ✅ COMPLETE
