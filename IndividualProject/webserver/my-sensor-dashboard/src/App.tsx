import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@material-ui/core';

type SensorData = {
  DHTTemperature: number;
  Humidity: number;
  LM35Temperature: number;
  Time: string;
};

const SensorTable: React.FC = () => {
  const [sensorData, setSensorData] = useState<SensorData[]>([]);

  useEffect(() => {
    axios.get('http://192.168.2.4:8080/api/v1/sensor-data')
      .then(response => {
        setSensorData(response.data);
      })
      .catch(error => console.error('Error fetching data: ', error));
  }, []);

  return (
    <TableContainer component={Paper}>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>DHT Temperature (°C)</TableCell>
            <TableCell>Humidity (%)</TableCell>
            <TableCell>LM35 Temperature (°C)</TableCell>
            <TableCell>Time</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {sensorData.map((row, index) => (
            <TableRow key={index}>
              <TableCell>{row.DHTTemperature}</TableCell>
              <TableCell>{row.Humidity}</TableCell>
              <TableCell>{row.LM35Temperature}</TableCell>
              <TableCell>{row.Time}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default SensorTable;
