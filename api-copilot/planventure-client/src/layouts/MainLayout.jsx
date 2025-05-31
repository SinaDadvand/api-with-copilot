import { Box } from '@mui/material';
import Navbar from '../components/navigation/Navbar';
import Footer from '../components/navigation/Footer';

const MainLayout = ({ children }) => {
  return (
    <Box sx={{ 
      display: 'flex', 
      flexDirection: 'column', 
      minHeight: '100vh',
      width: '100%',
      position: 'relative'
    }}>
      <Navbar />
      <Box 
        component="main" 
        sx={{ 
          flexGrow: 1,
          display: 'flex',
          flexDirection: 'column',
          width: '100%',
          minHeight: 'calc(100vh - 128px)', // Subtract navbar (64px) and footer (64px)
        }}
      >
        {children}
      </Box>
      <Footer />
    </Box>
  );
};

export default MainLayout;
