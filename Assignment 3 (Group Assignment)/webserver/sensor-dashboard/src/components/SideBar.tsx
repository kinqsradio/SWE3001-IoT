import React from 'react';
import { Drawer, List, ListItem, ListItemIcon, ListItemText, Typography } from '@mui/material';
import HomeIcon from '@mui/icons-material/Home';
import InfoIcon from '@mui/icons-material/Info';
import { Link } from 'react-router-dom';

const drawerWidth = 240; // Adjust the width of the sidebar

const Sidebar: React.FC = () => {
  return (
    <Drawer
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: drawerWidth,
          boxSizing: 'border-box',
        },
      }}
      variant="permanent"
      anchor="left"
    >
      <Typography variant="h6" sx={{ my: 2, mx: 2 }}>
        Sensor Dashboard
      </Typography>
      <List>
        {/* Link to Home */}
        <ListItem button component={Link} to="/">
          <ListItemIcon>
            <HomeIcon />
          </ListItemIcon>
          <ListItemText primary="Home" />
        </ListItem>
        
        {/* Link to About */}
        <ListItem button component={Link} to="/about">
          <ListItemIcon>
            <InfoIcon />
          </ListItemIcon>
          <ListItemText primary="About" />
        </ListItem>

        {/* Add more navigation links here */}
      </List>
    </Drawer>
  );
};

export default Sidebar;
