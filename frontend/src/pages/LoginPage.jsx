import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Container from '@mui/material/Container';
import Paper from '@mui/material/Paper';
import TextField from '@mui/material/TextField';
import Typography from '@mui/material/Typography';

export default function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleSubmit = e => {
    e.preventDefault();
    // TODO: authenticate via API
    navigate('/');
  };

  return (
    <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: '100vh', bgcolor: 'background.default' }}>
      <Container maxWidth="xs">
        <Paper elevation={3} sx={{ p: 3 }}>
          <Box component="form" onSubmit={handleSubmit} sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            <Typography variant="h5" component="h2" align="center">
              Вход
            </Typography>
            <TextField
              label="Имя пользователя"
              value={username}
              onChange={e => setUsername(e.target.value)}
              required
              fullWidth
            />
            <TextField
              label="Пароль"
              type="password"
              value={password}
              onChange={e => setPassword(e.target.value)}
              required
              fullWidth
            />
            <Button type="submit" variant="contained" fullWidth>
              Войти
            </Button>
          </Box>
        </Paper>
      </Container>
    </Box>
  );
}
