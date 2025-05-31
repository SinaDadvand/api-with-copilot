import React, { createContext, useContext, useState, useEffect } from 'react';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { CssBaseline } from '@mui/material';

const ThemeContext = createContext();

export const useAppTheme = () => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useAppTheme must be used within a ThemeContextProvider');
  }
  return context;
};

export const ThemeContextProvider = ({ children }) => {
  const [darkMode, setDarkMode] = useState(() => {
    // Check localStorage for saved preference
    const savedMode = localStorage.getItem('planventure-theme');
    if (savedMode) {
      return savedMode === 'dark';
    }
    // Default to system preference
    return window.matchMedia('(prefers-color-scheme: dark)').matches;
  });

  useEffect(() => {
    // Save theme preference to localStorage
    localStorage.setItem('planventure-theme', darkMode ? 'dark' : 'light');
  }, [darkMode]);

  const toggleTheme = () => {
    setDarkMode(prev => !prev);
  };
  const theme = createTheme({
    palette: {
      mode: darkMode ? 'dark' : 'light',
      primary: {
        main: darkMode ? '#58a6ff' : '#1976d2', // GitHub blue
        light: darkMode ? '#79c0ff' : '#42a5f5',
        dark: darkMode ? '#1f6feb' : '#1565c0',
      },
      secondary: {
        main: darkMode ? '#fd7e14' : '#dc004e', // GitHub orange
        light: darkMode ? '#ff8c42' : '#ff5983',
        dark: darkMode ? '#e8590c' : '#9a0036',
      },
      error: {
        main: darkMode ? '#f85149' : '#d32f2f', // GitHub red
        light: darkMode ? '#ff6b6b' : '#ef5350',
        dark: darkMode ? '#da3633' : '#c62828',
      },
      warning: {
        main: darkMode ? '#d29922' : '#ff9800', // GitHub yellow/orange
        light: darkMode ? '#f2cc60' : '#ffb74d',
        dark: darkMode ? '#9e6a03' : '#f57c00',
      },
      success: {
        main: darkMode ? '#3fb950' : '#4caf50', // GitHub green
        light: darkMode ? '#56d364' : '#66bb6a',
        dark: darkMode ? '#238636' : '#388e3c',
      },
      background: {
        default: darkMode ? '#0d1117' : '#fafafa', // GitHub dark background
        paper: darkMode ? '#161b22' : '#ffffff',   // GitHub dark paper
      },
      text: {
        primary: darkMode ? '#f0f6fc' : '#000000',   // GitHub text primary
        secondary: darkMode ? '#8b949e' : '#666666', // GitHub text secondary
      },
      divider: darkMode ? '#30363d' : '#e0e0e0', // GitHub border color
    },
    typography: {
      fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
      h4: {
        fontWeight: 600,
      },
      h5: {
        fontWeight: 500,
      },
    },    components: {
      MuiCard: {
        styleOverrides: {
          root: {
            border: darkMode ? '1px solid #30363d' : '1px solid #d0d7de',
            transition: 'transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out, border-color 0.2s ease-in-out',
            '&:hover': {
              transform: 'translateY(-2px)',
              borderColor: darkMode ? '#58a6ff' : '#1976d2',
              boxShadow: darkMode 
                ? '0 8px 25px 0 rgba(88, 166, 255, 0.15)' 
                : '0 8px 25px 0 rgba(0,0,0,0.15)',
            },
          },
        },
      },
      MuiPaper: {
        styleOverrides: {
          root: {
            backgroundImage: 'none',
            border: darkMode ? '1px solid #30363d' : 'none',
          },
        },
      },
      MuiButton: {
        styleOverrides: {
          root: {
            textTransform: 'none',
            borderRadius: '6px',
          },
          contained: {
            '&:hover': {
              transform: 'translateY(-1px)',
              boxShadow: darkMode 
                ? '0 4px 12px rgba(88, 166, 255, 0.3)' 
                : '0 4px 12px rgba(25, 118, 210, 0.3)',
            },
          },
        },
      },
    },
  });

  const contextValue = {
    darkMode,
    toggleTheme,
    theme,
  };

  return (
    <ThemeContext.Provider value={contextValue}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        {children}
      </ThemeProvider>
    </ThemeContext.Provider>
  );
};
