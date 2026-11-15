import React from 'react';
import { Card, Typography, Grid, Checkbox, Button } from '@mui/material';

interface ReviewGateProps {
  checklist: Array<{
    category: string;
    status: 'complete' | 'incomplete' | 'pending';
    description: string;
  }>;
  onReviewComplete: () => void;
}

export const IndependentReviewGate: React.FC<ReviewGateProps> = ({
  checklist,
  onReviewComplete
}) => {
  const [completed, setCompleted] = React.useState(false);
  
  const handleReview = () => {
    // Phase 12S: Independent Review Gate
    // Verify all checklist categories complete
    const allComplete = checklist.every(item => item.status === 'complete');
    
    if (allComplete) {
      setCompleted(true);
      onReviewComplete();
    } else {
      alert('Not all checklist categories complete');
    }
  };
  
  return (
    <div className="review-gate">
      <Typography variant="h5">Independent Review Gate</Typography>
      <Typography variant="body2">Phase 12S: Product Review & Judge Review & Technical Review</Typography>
      
      <Grid container spacing={2}>
        {checklist.map((item, index) => (
          <Grid item xs={12} md={6} key={index}>
            <Card className={`review-item ${item.status}`}>
              <Checkbox
                checked={item.status === 'complete'}
                disabled={item.status !== 'complete'}
              />
              <Typography variant="body1">{item.category}</Typography>
              <Typography variant="body2">{item.description}</Typography>
            </Card>
          </Grid>
        ))}
      </Grid>
      
      <Button
        variant="contained"
        color="primary"
        onClick={handleReview}
        disabled={completed}
      >
        {completed ? 'Review Complete' : 'Complete Review'}
      </Button>
      
      {completed && (
        <Typography variant="h6" className="review-complete">
          ✅ Milestone M4: Product Complete
        </Typography>
      )}
    </div>
  );
};

// Phase 12S Status: ✅ COMPLETE
