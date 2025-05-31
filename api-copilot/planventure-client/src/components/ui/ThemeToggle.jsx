import React from 'react';
import { IconButton, Tooltip } from '@mui/material';
import { Brightness4, Brightness7 } from '@mui/icons-material';
import { useAppTheme } from '../../context/ThemeContext';

const ThemeToggle = () => {
  const { darkMode, toggleTheme } = useAppTheme();

  return (
    <Tooltip title={`Switch to ${darkMode ? 'light' : 'dark'} mode`}>
      <IconButton 
        onClick={toggleTheme} 
        color="inherit"
        sx={{
          transition: 'all 0.3s ease-in-out',
          border: '1px solid transparent',
          '&:hover': {
            transform: 'rotate(180deg)',
            borderColor: 'primary.main',
            backgroundColor: 'rgba(255, 255, 255, 0.1)',
          },
        }}
      >
        {darkMode ? (
          <Brightness7 sx={{ color: '#ffd700' }} />
        ) : (
          <Brightness4 sx={{ color: '#555' }} />
        )}
      </IconButton>
    </Tooltip>
  );
};

export default ThemeToggle;
