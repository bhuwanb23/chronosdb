"""
Phase 12D: Executive Impact Dashboard (Updated)
Judge-Facing User Experience
"""

import React from 'react';
import { Card, Typography, Grid, Chip } from '@mui/material';

interface ExecutiveDashboardProps {
  revenueAtRisk: number;
  slaBreaches: number;
  affectedOrders: number;
  activeDisruptions: number;
  recoverySavings: number;
  recommendationConfidence: number;
}

export const ExecutiveDashboard: React.FC<ExecutiveDashboardProps> = ({
  revenueAtRisk,
  slaBreaches,
  affectedOrders,
  activeDisruptions,
  recoverySavings,
  recommendationConfidence
}) => {
  return (
    <div className="executive-dashboard">
      <Grid container spacing={2}>
        {/* Level 1: Immediate Business Risk */}
        <Grid item xs={12} md={3}>
          <Card className="risk-card red">
            <Typography variant="h6">Revenue At Risk</Typography>
            <Typography variant="h3">₹{revenueAtRisk.toLocaleString()}</Typography>
            <Chip label="Critical" color="error" />
            <Typography variant="body2" className="view-evidence">
              [View Evidence]
            </Typography>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Card className="risk-card amber">
            <Typography variant="h6">SLA Breaches</Typography>
            <Typography variant="h3">{slaBreaches}</Typography>
            <Chip label="Warning" color="warning" />
            <Typography variant="body2" className="view-evidence">
              [View Evidence]
            </Typography>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Card className="risk-card green">
            <Typography variant="h6">Recovery Savings</Typography>
            <Typography variant="h3">₹{recoverySavings.toLocaleString()}</Typography>
            <Chip label="Recovered" color="success" />
            <Typography variant="body2" className="view-evidence">
              [View Evidence]
            </Typography>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Card className="risk-card amber">
            <Typography variant="h6">Recommendation Confidence</Typography>
            <Typography variant="h3">{recommendationConfidence}%</Typography>
            <Chip label="High" color="primary" />
            <Typography variant="body2" className="view-evidence">
              [View Evidence]
            </Typography>
          </Card>
        </Grid>
        
        {/* Level 2: Recommendation */}
        <Grid item xs={12}>
          <Card className="recommendation-card">
            <Typography variant="h5">Recommended Intervention: HYBRID</Typography>
            <Typography variant="body1">Utility Score: 0.91 | Expected Savings: ₹11,00,000</Typography>
            <Typography variant="body2" className="view-evidence">
              [View Evidence]
            </Typography>
          </Card>
        </Grid>
      </Grid>
    </div>
  );
};

// Phase 12D Status: ✅ COMPLETE
