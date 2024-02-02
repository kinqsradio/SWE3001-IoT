import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import SensorDatata from './pages/SensorData';
import AboutPage from './pages/AboutPage';
import Sidebar from './components/SideBar';
import { Box } from '@mui/material';

function App() {
  return (
    <Router>
      <Box sx={{ display: 'flex' }}>
        <Sidebar />
        <Box
          component="main"
          sx={{ flexGrow: 1, bgcolor: 'background.default', p: 3 }}
        >
          <Routes>
            <Route path="/" element={<SensorDatata />} />
            <Route path="/about" element={<AboutPage />} />
            {/* Define other routes here */}
          </Routes>
        </Box>
      </Box>
    </Router>
  );
}

export default App;
