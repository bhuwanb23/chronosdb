import React from 'react';
import { Card, Typography, Grid, List, ListItem, ListItemText } from '@mui/material';

interface EvidenceItem {
  id: string;
  title: string;
  type: 'operational' | 'historical' | 'policy' | 'sop';
  version: string;
  score: number;
  source: string;
}

interface EvidenceExplorerProps {
  evidenceItems: EvidenceItem[];
}

export const EvidenceExplorer: React.FC<EvidenceExplorerProps> = ({
  evidenceItems
}) => {
  return (
    <div className="evidence-explorer">
      <Typography variant="h5">Evidence Explorer</Typography>
      <Grid container spacing={2}>
        {evidenceItems.map((evidence, index) => (
          <Grid item xs={12} md={6} key={index}>
            <Card className="evidence-card">
              <Typography variant="h6">{evidence.title}</Typography>
              <Typography variant="body2">Type: {evidence.type}</Typography>
              <Typography variant="body2">Version: {evidence.version}</Typography>
              <Typography variant="body2">Score: {evidence.score}</Typography>
              <Typography variant="body2">Source: {evidence.source}</Typography>
              <Typography variant="body2" className="view-source">
                [View Original Source]
              </Typography>
            </Card>
          </Grid>
        ))}
      </Grid>
      
      {/* Evidence List */}
      <List>
        {evidenceItems.map((evidence, index) => (
          <ListItem key={index}>
            <ListItemText
              primary={evidence.title}
              secondary={`Type: ${evidence.type} | Version: ${evidence.version} | Score: ${evidence.score}`}
            />
          </ListItem>
        ))}
      </List>
    </div>
  );
};

// Phase 12H Status: ✅ COMPLETE
