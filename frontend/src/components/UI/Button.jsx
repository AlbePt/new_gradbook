import React from 'react';
import { Button as MuiButton } from '@mui/material';

export default function Button({ variant = 'primary', ...props }) {
  const color =
    variant === 'secondary' ? 'secondary' : variant === 'text' ? 'inherit' : 'primary';
  const muiVariant = variant === 'text' ? 'text' : 'contained';

  return <MuiButton color={color} variant={muiVariant} {...props} />;
}
