import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Box, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Tooltip, Select, MenuItem, FormControl, InputLabel, TablePagination } from '@mui/material';
import { SelectChangeEvent } from '@mui/material/Select';
import { ReactElement } from 'react';
import { SensorDataItem, DeviceSensorData, useDeviceData } from './hooks/useDeviceData';


const SensorTable: React.FC = () => {
  const { devicesData, isLoading, error } = useDeviceData('https://r3n83zqx-9999.aue.devtunnels.ms/retrieve-all-sensor-data');
  const [selectedDeviceId, setSelectedDeviceId] = useState<string>('');
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(30);

  // Dynamically generate column order based on the selected device's data structure
  const generateColumnOrder = (deviceData: SensorDataItem[] | undefined) => {
    if (!deviceData || deviceData.length === 0) return ['Time'];

    const firstRowKeys = Object.keys(deviceData[0]);
    return ['Time', ...firstRowKeys.filter(key => key !== 'Time' && key !== 'DeviceID' && key !== 'id')];
  };

  // Setting default device ID based on devicesData
  useEffect(() => {
    if (devicesData.length > 0 && !selectedDeviceId) {
      // Optionally, prioritize selecting a specific device type if exists
      const defaultDeviceId = devicesData.find(device => device.device_id.includes('TemperatureHumidity_01'))?.device_id || devicesData[0].device_id;
      setSelectedDeviceId(defaultDeviceId);
    }
  }, [devicesData, selectedDeviceId]);

  const handleDeviceChange = (event: SelectChangeEvent<string>) => {
    setSelectedDeviceId(event.target.value);
    setPage(0); // Reset pagination
  };

  const handleChangePage = (_event: unknown, newPage: number) => setPage(newPage);
  const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  // Extract and paginate data for the selected device
  const selectedDeviceData = devicesData.find(device => device.device_id === selectedDeviceId)?.data || [];
  const columnOrder = generateColumnOrder(selectedDeviceData);
  const rows = selectedDeviceData.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage);


  // if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', overflow: 'hidden', height: '100%' }}>
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

      <TableContainer component={Paper} sx={{ maxHeight: 600, overflow: 'auto' }}>
        <Table stickyHeader aria-label={`Sensor data for ${selectedDeviceId}`} size="small">
          <TableHead>
            <TableRow>
              {columnOrder.map(column => (
                <TableCell key={column}>{column}</TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {rows.map((row, index) => (
              <TableRow key={index}>
                {columnOrder.map(column => (
                  <TableCell key={column}>
                    <Tooltip title={String(row[column])} placement="top">
                      <span>{String(row[column])}</span>
                    </Tooltip>
                  </TableCell>
                ))}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
      <TablePagination
        component="div"
        count={selectedDeviceData.length}
        rowsPerPage={rowsPerPage}
        page={page}
        onPageChange={handleChangePage}
        onRowsPerPageChange={handleChangeRowsPerPage}
      />
    </Box>
  );
};

export default SensorTable;
