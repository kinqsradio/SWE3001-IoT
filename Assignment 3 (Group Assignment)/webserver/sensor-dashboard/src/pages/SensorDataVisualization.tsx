import React, { useState, useEffect } from 'react';
import SensorDataChart from '../components/SensorDataVisualization'; // Ensure the path is correct based on your project structure
const SensorDataVisualization: React.FC = () => {
  return (
    <div>  
      <SensorDataChart />
    </div>
  );
};

export default SensorDataVisualization;