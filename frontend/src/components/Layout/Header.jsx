import React from 'react';
import { NavLink } from 'react-router-dom';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Button from '@mui/material/Button';
import IconButton from '@mui/material/IconButton';
import Box from '@mui/material/Box';
import MenuBookRoundedIcon from '@mui/icons-material/MenuBookRounded';
import AccountCircleRoundedIcon from '@mui/icons-material/AccountCircleRounded';

const menu = [
  { to: '/', label: 'Главная' },
  { to: '/journal', label: 'Журнал' },
  { to: '/planning', label: 'Планирование' },
  { to: '/admin', label: 'Панель управления' },
  { to: '/reports', label: 'Отчёты' },
];

export default function Header() {
  return (
    <AppBar position="fixed">
      <Toolbar>
        <MenuBookRoundedIcon sx={{ mr: 2 }} />
        <Box sx={{ flexGrow: 1, display: 'flex', gap: 2 }}>
          {menu.map(item => (
            <Button
              key={item.to}
              component={NavLink}
              to={item.to}
              color="inherit"
              sx={{ textTransform: 'none' }}
            >
              {item.label}
            </Button>
          ))}
        </Box>
        <Button component={NavLink} to="/help" color="inherit" sx={{ textTransform: 'none' }}>
          Справка
        </Button>
        <IconButton color="inherit">
          <AccountCircleRoundedIcon />
        </IconButton>
      </Toolbar>
    </AppBar>
  );
}
