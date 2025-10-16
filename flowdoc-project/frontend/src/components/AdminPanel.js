import React from 'react';
import { AppBar, Toolbar, Typography, IconButton } from '@material-ui/core';
import { Menu as MenuIcon } from '@material-ui/icons';

const AdminPanel = () => {
    return (
        <div>
            <AppBar position="static">
                <Toolbar>
                    <IconButton edge="start" color="inherit" aria-label="menu">
                        <MenuIcon />
                    </IconButton>
                    <Typography variant="h6">
                        Flowdoc Admin Panel
                    </Typography>
                </Toolbar>
            </AppBar>
            {/* Add your admin panel components here */}
        </div>
    );
};

export default AdminPanel;