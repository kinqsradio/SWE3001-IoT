import React, { useState, useEffect } from 'react';
import { Box, Paper, Typography, Select, MenuItem, FormControl, InputLabel, Snackbar, Button } from '@mui/material';
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
  
  const SensorNotification: React.FC = () => {
    const { devicesData } = useDeviceData('https://r3n83zqx-9999.aue.devtunnels.ms/retrieve-all-sensor-data');
    const [alarmQueue, setAlarmQueue] = useState<string[]>([]);
    const [currentAlarm, setCurrentAlarm] = useState<string | null>(null);
  
    useEffect(() => {
      const combinedAlarms = devicesData.flatMap(device =>
        checkForAlarms(device.data[0]) // Assuming the latest data for each device
      );
      if (combinedAlarms.length > 0) {
        setAlarmQueue(prevQueue => [...prevQueue, ...combinedAlarms]);
      }
    }, [devicesData]);
  
    useEffect(() => {
      if (!currentAlarm && alarmQueue.length > 0) {
        setCurrentAlarm(alarmQueue[0]);
        setAlarmQueue(prevQueue => prevQueue.slice(1));
      }
    }, [alarmQueue, currentAlarm]);
  
    const handleCloseSnackbar = () => {
      setCurrentAlarm(null); // Reset current alarm
    };
  
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
    
  
    return (
      <>
        {currentAlarm && (
          <Snackbar
            open={Boolean(currentAlarm)}
            autoHideDuration={6000}
            onClose={handleCloseSnackbar}
            message={currentAlarm}
            action={
              <Button color="secondary" size="small" onClick={handleCloseSnackbar}>
                Close
              </Button>
            }
          />
        )}
      </>
    );
  };
  
  export default SensorNotification;