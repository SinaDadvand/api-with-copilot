import { Box, Container, Paper, Fade } from '@mui/material';
import Navbar from '../components/navigation/Navbar';
import Footer from '../components/navigation/Footer';

const AuthLayout = ({ children }) => {
  return (
    <Box sx={{ 
      display: 'flex', 
      flexDirection: 'column', 
      minHeight: '100vh',
      width: '100%',
      position: 'relative',
      bgcolor: 'background.default'
    }}>
      <Navbar />
      
      {/* Main content area with centered auth forms */}
      <Container 
        component="main" 
        maxWidth="sm"
        sx={{ 
          flexGrow: 1,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          py: { xs: 2, sm: 4 },
          px: { xs: 2, sm: 3 },
          mt: { xs: 10, sm: 8 },
          mb: { xs: 8, sm: 10 }
        }}
      >
        <Fade in={true} timeout={500}>
          <Paper
            elevation={3}
            sx={{
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              bgcolor: 'background.paper',
              p: { xs: 3, sm: 4, md: 5 },
              borderRadius: 3,
              width: '100%',
              maxWidth: 400,
              position: 'relative',
              '&:hover': {
                boxShadow: (theme) => theme.shadows[6],
              },
              transition: 'box-shadow 0.3s ease-in-out'
            }}
          >
            {children}
          </Paper>
        </Fade>
      </Container>
      
      <Footer />
    </Box>
  );
};

export default AuthLayout;