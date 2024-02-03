import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import SensorData from './pages/SensorData';
import SensorDataVisualization from './pages/SensorDataVisualization';
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
            <Route path="/" element={<SensorData />} />
            <Route path="/visualisation" element={<SensorDataVisualization />} />
            {/* Define other routes here */}
          </Routes>
        </Box>
      </Box>
    </Router>
  );
}

export default App;
