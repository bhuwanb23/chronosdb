"""
Phase 12L: Error and Degraded States (Updated)
Judge-Facing User Experience
"""

import React from 'react';
import { Card, Typography, Box, Button } from '@mui/material';

interface ErrorStateProps {
  errorType: 'no_data' | 'missing_evidence' | 'simulation_failed' | 'db2_offline' | 'ai_offline' | 'audit_unavailable';
  recoveryAction: () => void;
}

export const ErrorState: React.FC<ErrorStateProps> = ({
  errorType,
  recoveryAction
}) => {
  const errorMessages = {
    'no_data': {
      title: 'No Data Available',
      message: 'No operational data found for this scenario.',
      action: 'Load Sample Data'
    },
    'missing_evidence': {
      title: 'Missing Evidence',
      message: 'Required evidence packages not found.',
      action: 'Retrieve Evidence'
    },
    'simulation_failed': {
      title: 'Simulation Failed',
      message: 'Counterfactual simulation could not complete.',
      action: 'Retry Simulation'
    },
    'db2_offline': {
      title: 'Db2 Offline',
      message: 'Database connection lost.',
      action: 'Reconnect'
    },
    'ai_offline': {
      title: 'AI Service Offline',
      message: 'Natural language processing unavailable.',
      action: 'Retry AI'
    },
    'audit_unavailable': {
      title: 'Audit Unavailable',
      message: 'Audit records not accessible.',
      action: 'Reload Audit'
    }
  };
  
  const errorInfo = errorMessages[errorType] || errorMessages['no_data'];
  
  return (
    <div className="error-state">
      <Card className="error-card">
        <Typography variant="h5">{errorInfo.title}</Typography>
        <Typography variant="body1">{errorInfo.message}</Typography>
        <Button
          variant="contained"
          color="primary"
          onClick={recoveryAction}
        >
          {errorInfo.action}
        </Button>
      </Card>
    </div>
  );
};

// Phase 12L Status: ✅ COMPLETE
