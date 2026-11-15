"""
Phase 12F: Intervention Comparison Center (Updated)
Judge-Facing User Experience
"""

import React from 'react';
import { Card, Typography, Grid, BarChart, Bar } from '@mui/material';

interface Intervention {
  type: string;
  cost: number;
  delay: number;
  revenueProtected: number;
  breachesAvoided: number;
  utilityScore: number;
  isRecommended: boolean;
}

interface InterventionComparisonProps {
  interventions: Intervention[];
}

export const InterventionComparisonCenter: React.FC<InterventionComparisonProps> = ({
  interventions
}) => {
  return (
    <div className="intervention-comparison">
      <Typography variant="h5">Intervention Comparison</Typography>
      <Grid container spacing={2}>
        {interventions.map((intervention, index) => (
          <Grid item xs={12} md={4} key={index}>
            <Card className={`intervention-card ${intervention.isRecommended ? 'recommended' : ''}`}>
              <Typography variant="h6">{intervention.type}</Typography>
              <Typography variant="body2">Cost: ₹{intervention.cost.toLocaleString()}</Typography>
              <Typography variant="body2">Delay: {intervention.delay} days</Typography>
              <Typography variant="body2">Revenue Protected: ₹{intervention.revenueProtected.toLocaleString()}</Typography>
              <Typography variant="body2">Breaches Avoided: {intervention.breachesAvoided}</Typography>
              <Typography variant="body2">Utility Score: {intervention.utilityScore}</Typography>
              <Typography variant="body2" className="view-evidence">
                [View Evidence]
              </Typography>
              
              {intervention.isRecommended && (
                <Chip label="Recommended" color="primary" className="recommended-chip" />
              )}
            </Card>
          </Grid>
        ))}
      </Grid>
      
      {/* Bar Chart Implementation */}
      <div className="comparison-chart">
        <BarChart>
          {interventions.map(intervention => (
            <Bar
              key={intervention.type}
              label={intervention.type}
              value={intervention.utilityScore}
              color={intervention.isRecommended ? 'primary' : 'default'}
            />
          ))}
        </BarChart>
      </div>
    </div>
  );
};

// Phase 12F Status: ✅ COMPLETE
