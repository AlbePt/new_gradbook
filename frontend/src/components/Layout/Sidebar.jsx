import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import IconButton from '@mui/material/IconButton';
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
import MenuRoundedIcon from '@mui/icons-material/MenuRounded';

const links = [
  { to: 'subjects', label: 'Предметы' },
  { to: 'teachers', label: 'Преподаватели' },
];

export default function Sidebar() {
  const [open, setOpen] = useState(true);

  if (!open) {
    return (
      <Box sx={{ p: 1 }}>
        <IconButton onClick={() => setOpen(true)} size="large">
          <MenuRoundedIcon />
        </IconButton>
      </Box>
    );
  }

  return (
    <Paper className="sidebar" elevation={0}>
      <Box sx={{ display: 'flex', justifyContent: 'flex-end', p: 1 }}>
        <IconButton onClick={() => setOpen(false)} size="large">
          <MenuRoundedIcon />
        </IconButton>
      </Box>
      <List>
        {links.map(link => (
          <ListItem key={link.label} disablePadding>
            <ListItemButton component={NavLink} to={link.to}>
              <ListItemText primary={link.label} />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
    </Paper>
  );
}
