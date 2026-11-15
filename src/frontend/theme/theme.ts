"""
Phase 12M: Visual Design System (Updated)
Judge-Facing User Experience
"""

// Phase 12M: ChronosDB Theme
// Operations Center / Control Tower / Decision Intelligence
// Avoid: Consumer chatbot look
// Design Language: Dark Theme, Data-focused, Enterprise Dashboard, Minimal gradients, High contrast
// Typography: Inter, IBM Plex Sans

export const theme = {
  palette: {
    mode: 'dark',
    primary: {
      main: '#007bff', // Enterprise blue
      contrastText: '#ffffff'
    },
    secondary: {
      main: '#6f42c1', // Decision intelligence purple
      contrastText: '#ffffff'
    },
    error: {
      main: '#dc3545', // Risk red
      contrastText: '#ffffff'
    },
    warning: {
      main: '#ffc107', // Warning amber
      contrastText: '#000000'
    },
    success: {
      main: '#28a745', // Recovered green
      contrastText: '#ffffff'
    },
    background: {
      default: '#121212', // Dark theme
      paper: '#1e1e1e'
    },
    text: {
      primary: '#ffffff',
      secondary: '#b0b0b0'
    }
  },
  typography: {
    fontFamily: '"Inter", "IBM Plex Sans", sans-serif',
    h5: {
      fontWeight: 600,
      fontSize: '1.25rem'
    },
    h6: {
      fontWeight: 600,
      fontSize: '1rem'
    },
    body1: {
      fontSize: '0.875rem'
    },
    body2: {
      fontSize: '0.75rem'
    }
  },
  components: {
    MuiCard: {
      styleOverrides: {
        root: {
          backgroundColor: '#1e1e1e',
          borderRadius: 8,
          padding: 16,
          border: '1px solid #333'
        }
      }
    },
    MuiTypography: {
      styleOverrides: {
        root: {
          color: '#ffffff'
        }
      }
    }
  }
};

// Phase 12M Status: ✅ COMPLETE
