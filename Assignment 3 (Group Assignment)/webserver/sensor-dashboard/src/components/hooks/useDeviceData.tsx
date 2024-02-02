// In useDeviceData.ts or wherever the hook is defined

import { useState, useEffect } from 'react';
import axios from 'axios';

export interface SensorDataItem {
  DeviceID: string;
  DHTTemperature?: number;
  Humidity?: number;
  LM35Temperature?: number;
  Time: string;
  id: number;
  [key: string]: any;
}

export interface DeviceSensorData {
  data: SensorDataItem[];
  device_id: string;
}

export const useDeviceData = (apiUrl: string, pollInterval: number = 10000): { devicesData: DeviceSensorData[], isLoading: boolean, error: Error | null } => {
  const [devicesData, setDevicesData] = useState<DeviceSensorData[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      setIsLoading(true);
      try {
        const response = await axios.get<DeviceSensorData[]>(apiUrl);
        setDevicesData(response.data);
        setError(null);
      } catch (error) {
        setError(error as Error);
      } finally {
        setIsLoading(false);
      }
    };

    // Initial data fetch
    fetchData();

    // Set up polling with the specified interval
    const intervalId = setInterval(fetchData, pollInterval);

    // Cleanup function to clear interval when the component unmounts or apiUrl changes
    return () => clearInterval(intervalId);
  }, [apiUrl, pollInterval]); // Depend on apiUrl and pollInterval to refetch if they change

  return { devicesData, isLoading, error };
};
