import React from 'react';
import SensorTable from '../components/SensorTable'; // Ensure the path is correct based on your project structure

const HomePage: React.FC = () => {
  return (
    <div>
      <h1>Home Page</h1>
      {/* Other homepage content here */}
      
      {/* SensorTable component included */}
      <SensorTable />
    </div>
  );
};

export default HomePage;
