import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import { TextField, Box, Typography } from '@mui/material';
import Button from '../components/UI/Button.jsx';

const schema = yup.object({
  username: yup.string().required('Обязательное поле'),
  password: yup.string().required('Обязательное поле')
});

export default function LoginPage() {
  const navigate = useNavigate();
  const {
    register,
    handleSubmit,
    formState: { errors }
  } = useForm({ resolver: yupResolver(schema) });

  const onSubmit = () => {
    // TODO: authenticate via API
    navigate('/');
  };

  return (
    <Box sx={{ maxWidth: 360, mx: 'auto', mt: 8 }}>
      <Typography variant="h5" component="h1" align="center" gutterBottom>
        Вход
      </Typography>
      <Box component="form" onSubmit={handleSubmit(onSubmit)} noValidate>
        <TextField
          label="Имя пользователя"
          fullWidth
          margin="normal"
          {...register('username')}
          error={Boolean(errors.username)}
          helperText={errors.username?.message}
        />
        <TextField
          label="Пароль"
          type="password"
          fullWidth
          margin="normal"
          {...register('password')}
          error={Boolean(errors.password)}
          helperText={errors.password?.message}
        />
        <Button type="submit" fullWidth sx={{ mt: 2 }}>
          Войти
        </Button>
      </Box>
    </Box>
  );
}
