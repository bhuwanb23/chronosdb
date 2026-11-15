import React from 'react';
import { Slider, Typography, Box, Card } from '@mui/material';

interface ReplayStage {
  stage: string;
  timestamp: string;
  facts: string[];
  evidence: string[];
  decisionState: string;
}

interface TimelineAndReplayProps {
  stages: ReplayStage[];
  onStageChange: (stageIndex: number) => void;
}

export const TimelineAndDecisionReplay: React.FC<TimelineAndReplayProps> = ({
  stages,
  onStageChange
}) => {
  const [currentStage, setCurrentStage] = React.useState(0);
  
  const handleSliderChange = (event: Event, value: number | number[]) => {
    const stageIndex = typeof value === 'number' ? value : value[0];
    setCurrentStage(stageIndex);
    onStageChange(stageIndex);
  };
  
  const current = stages[currentStage] || stages[0];
  
  return (
    <div className="timeline-replay">
      <Typography variant="h5">Timeline and Decision Replay</Typography>
      
      {/* Interactive Slider */}
      <Box className="replay-slider">
        <Slider
          value={currentStage}
          min={0}
          max={stages.length - 1}
          step={1}
          marks
          onChange={handleSliderChange}
          valueLabelDisplay="auto"
        />
      </Box>
      
      {/* Current Stage Display */}
      <Card className="replay-stage">
        <Typography variant="h6">{current.stage}</Typography>
        <Typography variant="body2">Timestamp: {current.timestamp}</Typography>
        
        <Typography variant="subtitle1">Known Facts</Typography>
        <ul>
          {current.facts.map((fact, index) => (
            <li key={index}>{fact}</li>
          ))}
        </ul>
        
        <Typography variant="subtitle1">Evidence</Typography>
        <ul>
          {current.evidence.map((evidence, index) => (
            <li key={index}>{evidence}</li>
          ))}
        </ul>
        
        <Typography variant="subtitle1">Decision State</Typography>
        <Typography variant="body1">{current.decisionState}</Typography>
      </Card>
    </div>
  );
};

// Phase 12G Status: ✅ COMPLETE
