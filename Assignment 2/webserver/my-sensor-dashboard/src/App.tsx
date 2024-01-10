import React, { useEffect, useState } from 'react';
import axios from 'axios';
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  TablePagination
} from '@material-ui/core';
import { Line } from 'react-chartjs-2';
import 'chart.js/auto';
import { CSSProperties } from 'react';

type SensorData = {
  DHTTemperature: number;
  Humidity: number;
  LM35Temperature: number;
  Time: string;
};

const SensorTable: React.FC = () => {
  const [sensorData, setSensorData] = useState<SensorData[]>([]);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(25); // Set Max Shown on Table
  const [focusedButton, setFocusedButton] = useState<string | null>(null);


  const fetchData = () => {
    axios.get('http://192.168.2.4:8080/api/v1/sensor-data')
      .then(response => {
        setSensorData(response.data);
      })
      .catch(error => console.error('Error fetching data: ', error));
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 5000); // Fetch data every 5 seconds
    return () => clearInterval(interval); // Cleanup on unmount
  }, []);

  const handleChangePage = (event: unknown, newPage: number) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
    setRowsPerPage(+event.target.value);
    setPage(0);
  };

  const handleCalculateMean = (dataKey: keyof SensorData) => {
    const mean = sensorData.reduce((acc, data) => acc + Number(data[dataKey]), 0) / sensorData.length;
    alert(`Mean ${dataKey}: ${mean.toFixed(2)}`);
  };

  const buttonStyle = (key: string): CSSProperties => ({
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    padding: '6px 14px',
    fontFamily: '-apple-system, BlinkMacSystemFont, "Roboto", sans-serif',
    borderRadius: '6px',
    color: '#3D3D3D',
    background: '#fff',
    border: 'none',
    boxShadow: focusedButton === key ? '0px 0.5px 1px rgba(0, 0, 0, 0.1), 0px 0px 0px 3.5px rgba(58, 108, 217, 0.5)' : '0px 0.5px 1px rgba(0, 0, 0, 0.1)',
    userSelect: 'none',
    WebkitUserSelect: 'none',
    touchAction: 'manipulation',
    outline: 0
  });

  const chartData = (label: string, dataKey: keyof SensorData, color: string) => ({
    labels: sensorData.map(data => data.Time),
    datasets: [{
      label: label,
      data: sensorData.map(data => data[dataKey]),
      fill: false,
      borderColor: color,
      tension: 0.1
    }]
  });

  return (
    <>
      {/* Header - Fixed position */}
      <header style={{ textAlign: 'center', padding: '10px', position: 'absolute', top: 0, width: '100%', zIndex: 1000 }}>
        <h1>Sensor Data Visualization</h1>
      </header>

      {/* Main content container */}
      <div style={{ maxWidth: '95%', margin: '80px auto 20px', padding: '0 20px' }}>
        
        {/* Charts with Buttons */}
        <div style={{ display: 'flex', justifyContent: 'space-around', flexWrap: 'wrap', marginBottom: '20px' }}>
          
          {/* Mapping through each sensor data key for charts and buttons */}
          {['DHTTemperature', 'Humidity', 'LM35Temperature'].map((key, index) => (
            <div key={index} style={{ flexBasis: '30%', flexGrow: 1, minWidth: '250px', maxWidth: '400px', marginBottom: '20px' }}>
              <Line data={chartData(`${key} (°C)`, key as keyof SensorData, ['rgb(75, 192, 192)', 'rgb(54, 162, 235)', 'rgb(255, 99, 132)'][index])} />
              <div style={{ textAlign: 'center', marginTop: '10px' }}>
                <button 
                  onClick={() => handleCalculateMean(key as keyof SensorData)}
                  style={buttonStyle(key)}
                  onFocus={() => setFocusedButton(key)}
                  onBlur={() => setFocusedButton(null)}
                >
                  Calculate Mean {key}
                </button>
              </div>
            </div>
          ))}
        </div>


      {/* Table for displaying sensor data */}
      <TableContainer component={Paper} style={{ maxHeight: 650}}>
        <Table stickyHeader>
          <TableHead>
            <TableRow>
              {Object.keys(sensorData[0] || {}).map((header, index) => (
                <TableCell key={index}>{header}</TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {sensorData.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage).map((row, index) => (
              <TableRow key={index}>
                {Object.values(row).map((value, cellIndex) => (
                  <TableCell key={cellIndex}>{value}</TableCell>
                ))}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      {/* Pagination for the table */}
      <TablePagination
        component="div"
        rowsPerPageOptions={[25, 50, 100]}
        count={sensorData.length}
        rowsPerPage={rowsPerPage}
        page={page}
        onPageChange={handleChangePage}
        onRowsPerPageChange={handleChangeRowsPerPage}
      />
      </div>

      {/* Footer */}
      <footer style={{ textAlign: 'center', position: 'sticky', bottom: 0, backgroundColor: '#f8f8f8', padding: '10px'}}>
        <p>© Tran Duc Anh Dang: 103995439 - Sensor Data Dashboard</p>
      </footer>
    </>
  );
};

export default SensorTable;
