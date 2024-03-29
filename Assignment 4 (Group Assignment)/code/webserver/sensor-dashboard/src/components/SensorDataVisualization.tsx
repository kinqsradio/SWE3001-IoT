
import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import { Box, FormControl, InputLabel, Select, MenuItem, Typography, TextField } from '@mui/material';
import { SelectChangeEvent } from '@mui/material/Select';
import { useDeviceData, DeviceSensorData } from './hooks/useDeviceData';

import { 
  Chart as ChartJS, 
  CategoryScale, 
  LinearScale, 
  BarElement, 
  LineElement, 
  PointElement, 
  Title, 
  Tooltip, 
  Legend,
  TimeScale,
  ChartData 
} from 'chart.js';
import 'chartjs-adapter-date-fns';
import { format, startOfDay, endOfDay } from 'date-fns';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  Title,
  Tooltip,
  Legend,
  TimeScale
);


const SensorDataChart: React.FC = () => {
  const apiUrl = 'https://r3n83zqx-9999.aue.devtunnels.ms/retrieve-all-sensor-data';
  const { devicesData, isLoading, error } = useDeviceData(apiUrl);
  const [selectedDeviceId, setSelectedDeviceId] = useState<string>('');
  const [selectedDate, setSelectedDate] = useState<string>(format(new Date(), 'yyyy-MM-dd'));

  useEffect(() => {
    if (devicesData.length > 0 && !selectedDeviceId) {
      const defaultDeviceId = devicesData.find(device => device.device_id.includes('TemperatureHumidity_01'))?.device_id || devicesData[0].device_id;
      setSelectedDeviceId(defaultDeviceId);
    }
  }, [devicesData, selectedDeviceId]);

  const handleDeviceChange = (event: SelectChangeEvent<string>) => {
    setSelectedDeviceId(event.target.value);
  };  

  const handleDateChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSelectedDate(event.target.value);
  };

  const generateChartData = (): ChartData<'line'> => {
    const selectedDevice = devicesData.find(device => device.device_id === selectedDeviceId);
    if (!selectedDevice) {
      return { datasets: [] }; 
    }
  
    // Sort data by time to ensure chronological order
    const sortedData = selectedDevice.data.sort((a, b) => new Date(a.Time).getTime() - new Date(b.Time).getTime());
  
    // Generate datasets dynamically based on the sorted data
    const datasets = Object.keys(sortedData[0])
      .filter(key => key !== 'DeviceID' && key !== 'Time' && key !== 'id')
      .map((key, index) => {
        // Map data points for each key, excluding non-data properties
        const dataPoints = sortedData.map(data => {
          // Convert time to a suitable format for the x-axis
          const xValue = new Date(data.Time).getTime();
          let yValue;
  
          // Check if the key's value is numeric or text
          if (typeof data[key] === 'number') {
            yValue = data[key];
          } else {
            // For text data, map "Motion Detected" to 1, otherwise 0
            yValue = data[key] === "Motion detected" ? 1 : 0;
          }
  
          return { x: xValue, y: yValue };
        });
  
        return {
          label: key, 
          data: dataPoints,
          borderColor: `hsl(${index * 137.508}, 70%, 50%)`,
          backgroundColor: `hsla(${index * 137.508}, 70%, 50%, 0.5)`,
          fill: false,
        };
      });
  
    return {
      labels: sortedData.map(data => new Date(data.Time).toISOString()),
      datasets,
    };
  };
  

  const chartData = generateChartData();

  return (
    <Box>
      <Typography variant="h6" sx={{ marginBottom: 2 }}>Sensor Data Visualization</Typography>
      <FormControl fullWidth margin="normal">
        <InputLabel id="device-select-label">Select Device</InputLabel>
        <Select
          labelId="device-select-label"
          value={selectedDeviceId}
          onChange={handleDeviceChange}
          label="Select Device"
        >
          {devicesData.map(device => (
            <MenuItem key={device.device_id} value={device.device_id}>{device.device_id}</MenuItem>
          ))}
        </Select>
      </FormControl>
      <TextField
        label="Select Date"
        type="date"
        defaultValue={selectedDate}
        onChange={handleDateChange}
        fullWidth
        sx={{ mb: 2 }}
        InputLabelProps={{
          shrink: true,
        }}
      />
      {chartData && (
        <Line data={chartData} options={{
          responsive: true,
          scales: {
            x: {
              type: 'time',
              time: {
                unit: 'day',
                tooltipFormat: 'yyyy-MM-dd HH:mm:ss',
              },
              title: { display: true, text: 'Time' }
            },
            y: {
              beginAtZero: true,
              title: { display: true, text: 'Value' }
            }
          },
          animation: {
            duration: 800,
            easing: 'easeInOutQuad',
          },
        }} />
      )}
    </Box>
  );
};

export default SensorDataChart;