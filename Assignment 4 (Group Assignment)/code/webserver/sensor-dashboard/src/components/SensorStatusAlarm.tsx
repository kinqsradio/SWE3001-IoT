import React, { useState, useEffect } from 'react';
import { Box, Paper, Typography, Select, MenuItem, FormControl, InputLabel, Snackbar } from '@mui/material';
import { SelectChangeEvent } from '@mui/material/Select';
import { useDeviceData, DeviceSensorData, SensorDataItem } from './hooks/useDeviceData';
  
  
interface NumericThreshold {
    threshold: number;
    condition: 'above' | 'below';
}
  
interface TextThreshold {
    expected: string;
}
  
  type SensorThreshold = NumericThreshold | TextThreshold;
  
  const thresholds: Record<string, SensorThreshold> = {
    DHTTemperature: { threshold: 20, condition: 'above' },
    Humidity: { threshold: 60, condition: 'above' },
    LM35Temperature: { threshold: 20, condition: 'above' },
    WaterLevel: { threshold: 60, condition: 'above' },
    MotionStatus: { expected: "Motion detected" },
  };
  
const SensorStatusAlarm: React.FC = () => {
  const { devicesData, isLoading, error } = useDeviceData('https://r3n83zqx-9999.aue.devtunnels.ms/retrieve-all-sensor-data');
  const [selectedDeviceId, setSelectedDeviceId] = useState<string>('');
  const [open, setOpen] = useState(false);
  const [alarmMessage, setAlarmMessage] = useState("");


  useEffect(() => {
    if (devicesData.length > 0 && !selectedDeviceId) {
        const defaultDeviceId = devicesData.find(device => device.device_id.includes('TemperatureHumidity_01'))?.device_id || devicesData[0].device_id;
        setSelectedDeviceId(defaultDeviceId);
    }
  }, [devicesData, selectedDeviceId]);

  const handleDeviceChange = (event: SelectChangeEvent<string>) => {
    setSelectedDeviceId(event.target.value);
  };

  // Dynamically determine if any sensor data exceeds thresholds or meets specific conditions
  const checkForAlarms = (sensorData: SensorDataItem): string[] => {
    return Object.entries(sensorData)
      .filter(([key]) => key !== 'DeviceID' && key !== 'Time' && key !== 'id')
      .map(([key, value]) => {
        const condition = thresholds[key];
  
        // Handling numeric conditions
        if (condition && 'threshold' in condition && typeof value === 'number') {
          const isAlarm = condition.condition === 'above' ? value > condition.threshold : value < condition.threshold;
          if (isAlarm) {
            return `${key} is ${condition.condition} threshold (${condition.threshold}), current: ${value}`;
          }
        }
  
        // Handling text-based conditions
        if (condition && 'expected' in condition && typeof value === 'string') {
          if (value === condition.expected) {
            return `${key}: ${value}`;
          }
        }
  
        return null;
      })
      .filter((message): message is string => message !== null); // Filter out nulls
  };

  const getLatestData = (deviceData: DeviceSensorData[]) => {
    const latestData = deviceData.map(device => ({
      ...device,
      data: device.data.sort((a, b) => b.Time.localeCompare(a.Time))
    }));
    return latestData;
  };

  const latestDevicesData = getLatestData(devicesData);
  const selectedDeviceData = latestDevicesData.find(device => device.device_id === selectedDeviceId);
  const alarms = selectedDeviceData ? checkForAlarms(selectedDeviceData.data[0]) : []; // Checking only the first (latest) entry
  
  
  return (
    <Box sx={{ padding: 2 }}>
      <Typography variant="h6" sx={{ marginBottom: 2 }}>Sensor Status and Alarms</Typography>
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
      <Paper elevation={3} sx={{ padding: 2, marginTop: 2 }}>
        {alarms.length > 0 ? alarms.map((alarm, index) => (
          <Typography key={index} color="error">{alarm}</Typography>
        )) : (
          <Typography>All clear, no alarms.</Typography>
        )}
      </Paper>
    </Box>
  );
};

export default SensorStatusAlarm;