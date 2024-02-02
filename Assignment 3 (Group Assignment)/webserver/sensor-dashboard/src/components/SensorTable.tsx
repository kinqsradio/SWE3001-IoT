import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Box, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from '@mui/material';

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
    <Box sx={{ display: 'flex', overflowX: 'auto', maxWidth: '100%', mt: 2 }}>
      {devicesData.map((device) => (
        <TableContainer component={Paper} key={device.device_id} sx={{ minWidth: 300, mx: 2 }}>
          <Table aria-label={`Sensor data for ${device.device_id}`} size="small">
            <TableHead>
              <TableRow>
                <TableCell>Time</TableCell>
                {Object.keys(device.data[0]).filter(key => key !== 'DeviceID' && key !== 'id' && key !== 'Time').map((key) => (
                  <TableCell key={key}>{key}</TableCell>
                ))}
              </TableRow>
            </TableHead>
            <TableBody>
              {device.data.map((row, index) => (
                <TableRow key={index}>
                  <TableCell>{row.Time}</TableCell>
                  {Object.keys(row).filter(key => key !== 'DeviceID' && key !== 'id' && key !== 'Time').map((key) => (
                    <TableCell key={key}>{String(row[key])}</TableCell>
                  ))}
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      ))}
    </Box>
  );
};

export default SensorTable;
