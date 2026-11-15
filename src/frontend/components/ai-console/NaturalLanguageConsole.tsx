import React, { useState } from 'react';
import { TextField, Button, Box, Typography, Paper } from '@mui/material';

interface NaturalLanguageConsoleProps {
  onQuerySubmit: (query: string) => void;
}

export const NaturalLanguageConsole: React.FC<NaturalLanguageConsoleProps> = ({
  onQuerySubmit
}) => {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  
  const handleSubmit = async () => {
    if (!query.trim()) return;
    
    setLoading(true);
    
    // Phase 11I: AI Orchestration Service integration
    // POST /api/v1/explain
    try {
      const responseData = await fetch('/api/v1/explain', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query })
      });
      
      const result = await responseData.json();
      if (result.status === 'SUCCESS') {
        setResponse(result.data.narrative);
      } else {
        setResponse('Error: ' + result.data.message);
      }
    } catch (error) {
      setResponse('System error occurred');
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <div className="ai-console">
      <Typography variant="h6">Natural Language Console</Typography>
      <Box className="console-container">
        <TextField
          fullWidth
          variant="outlined"
          placeholder="Supplier S-104 down for two weeks..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyPress={(e) => {
            if (e.key === 'Enter') handleSubmit();
          }}
        />
        <Button
          variant="contained"
          onClick={handleSubmit}
          disabled={loading}
        >
          {loading ? 'Processing...' : 'Explain'}
        </Button>
        
        {response && (
          <Paper className="response-container">
            <Typography variant="body1">{response}</Typography>
          </Paper>
        )}
      </Box>
    </div>
  );
};

// Phase 12J Status: ✅ COMPLETE
