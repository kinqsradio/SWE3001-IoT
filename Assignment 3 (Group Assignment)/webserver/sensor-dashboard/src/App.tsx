interface SensorDataItem {
  DeviceID: string;
  MotionStatus?: string;
  DHTTemperature?: number;
  Humidity?: number;
  LM35Temperature?: number;
  WaterLevel?: number;
  Time: string;
  id: number;
  [key: string]: any; 
}


interface DeviceSensorData {
  data: SensorDataItem[];
  device_id: string;
}


import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';

const SensorTable: React.FC = () => {
  const [devicesData, setDevicesData] = useState<DeviceSensorData[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get<DeviceSensorData[]>('https://r3n83zqx-9999.aue.devtunnels.ms/retrieve-all-sensor-data');
        setDevicesData(response.data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  return (
    <div>
      {devicesData.map((device) => (
        <TableContainer component={Paper} key={device.device_id} style={{ marginBottom: '20px' }}>
          <Table aria-label="simple table">
            <TableHead>
              <TableRow>
                <TableCell>Time</TableCell>
                <TableCell>Device ID</TableCell>
                {Object.keys(device.data[0]).filter(key => key !== 'DeviceID' && key !== 'id' && key !== 'Time').map((key) => (
                  <TableCell key={key}>{key}</TableCell>
                ))}
              </TableRow>
            </TableHead>
            <TableBody>
              {device.data.map((row, index) => (
                <TableRow key={index}>
                  <TableCell>{row.Time}</TableCell>
                  <TableCell>{row.DeviceID}</TableCell>
                  {Object.keys(row).filter(key => key !== 'DeviceID' && key !== 'id' && key !== 'Time').map((key) => (
                    <TableCell key={key}>{String(row[key])}</TableCell>
                  ))}
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      ))}
    </div>
  );
};

export default SensorTable;
