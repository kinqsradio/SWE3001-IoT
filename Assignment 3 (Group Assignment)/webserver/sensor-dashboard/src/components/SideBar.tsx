import React, { useState, useEffect } from 'react';
import { Drawer, List, ListItem, ListItemIcon, ListItemText, Typography, useTheme } from '@mui/material';
import HomeIcon from '@mui/icons-material/Home';
import InfoIcon from '@mui/icons-material/Info';
import { Link, useLocation } from 'react-router-dom';

const drawerWidth = 240; // Adjust the width of the sidebar

const Sidebar: React.FC = () => {
    const theme = useTheme();
    const location = useLocation();
    const [currentTime, setCurrentTime] = useState(new Date().toLocaleTimeString());

    useEffect(() => {
        const interval = setInterval(() => setCurrentTime(new Date().toLocaleTimeString()), 1000);
        return () => clearInterval(interval);
    }, []);

    const isCurrentPath = (path: string): boolean => location.pathname === path;

    return (
        <Drawer
            sx={{
                width: drawerWidth,
                flexShrink: 0,
                '& .MuiDrawer-paper': {
                    width: drawerWidth,
                    boxSizing: 'border-box',
                    backgroundColor: theme.palette.background.default, // Use theme's background color
                    color: theme.palette.text.primary, // Use theme's text color
                },
            }}
            variant="permanent"
            anchor="left"
        >
            <Typography variant="h6" sx={{ mx: 2, my: 3, fontWeight: 'medium' }}>
                Time: {currentTime}
            </Typography>
            <List>
                <ListItem button component={Link} to="/" sx={{ bgcolor: isCurrentPath('/') ? theme.palette.action.selected : 'inherit' }}>
                    <ListItemIcon>
                        <HomeIcon color={isCurrentPath('/') ? 'primary' : 'inherit'} />
                    </ListItemIcon>
                    <ListItemText primary="Sensor Data" />
                </ListItem>

                <ListItem button component={Link} to="/visualisation" sx={{ bgcolor: isCurrentPath('/visualisation') ? theme.palette.action.selected : 'inherit' }}>
                    <ListItemIcon>
                        <InfoIcon color={isCurrentPath('/visualisation') ? 'primary' : 'inherit'} />
                    </ListItemIcon>
                    <ListItemText primary="Sensor Chart" />
                </ListItem>

                <ListItem button component={Link} to="/status" sx={{ bgcolor: isCurrentPath('/status') ? theme.palette.action.selected : 'inherit' }}>
                    <ListItemIcon>
                        <InfoIcon color={isCurrentPath('/status') ? 'primary' : 'inherit'} />
                    </ListItemIcon>
                    <ListItemText primary="Status and Alarm" />
                </ListItem>

                {/* Add more navigation links here */}
            </List>
        </Drawer>
    );
};

export default Sidebar;
