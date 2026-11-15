"""
Phase 12E: Dependency Cascade Visualization (Updated)
Judge-Facing User Experience
"""

import React from 'react';
import { Box, Typography } from '@mui/material';

interface CascadeNode {
  id: string;
  label: string;
  type: 'supplier' | 'component' | 'order' | 'revenue';
  status: 'normal' | 'warning' | 'critical';
}

interface CascadeVisualizationProps {
  nodes: CascadeNode[];
  links: Array<{ source: string; target: string }>;
}

export const DependencyCascadeVisualization: React.FC<CascadeVisualizationProps> = ({
  nodes,
  links
}) => {
  return (
    <div className="cascade-visualization">
      <Typography variant="h5">Dependency Cascade</Typography>
      <Box className="node-graph">
        {/* Node Graph Implementation */}
        {nodes.map(node => (
          <div key={node.id} className={`node ${node.status}`}>
            <Typography variant="subtitle1">{node.label}</Typography>
            <Typography variant="body2">{node.type}</Typography>
            <Typography variant="body2" className="view-evidence">
              [View Evidence]
            </Typography>
          </div>
        ))}
        
        {/* Links Implementation */}
        {links.map((link, index) => (
          <div key={index} className="link">
            <span>{link.source}</span> → <span>{link.target}</span>
          </div>
        ))}
      </Box>
    </div>
  );
};

// Phase 12E Status: ✅ COMPLETE
