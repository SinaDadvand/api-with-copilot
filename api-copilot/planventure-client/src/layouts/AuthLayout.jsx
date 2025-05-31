import { Box, Container } from '@mui/material';

const AuthLayout = ({ children }) => {
  return (
    <Box sx={{ 
      display: 'flex', 
      alignItems: 'center', 
      justifyContent: 'center', 
      minHeight: 'calc(100vh - 128px)',
      width: '100%',
      py: 4,
      bgcolor: 'background.default'
    }}>
      <Container 
        component="main" 
        maxWidth="xs"
        sx={{ 
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          px: { xs: 2, sm: 3 }
        }}
      >
        <Box
          sx={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            bgcolor: 'background.paper',
            p: 4,
            borderRadius: 2,
            boxShadow: 1,
            width: '100%'
          }}
        >
          {children}
        </Box>
      </Container>
    </Box>
  );
};

export default AuthLayout;