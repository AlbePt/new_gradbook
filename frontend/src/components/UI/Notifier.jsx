import React, { useState } from 'react';
import { Snackbar, Alert } from '@mui/material';

export default function Notifier() {
  const [message, setMessage] = useState(null);
  const handleClose = () => setMessage(null);

  return (
    <Snackbar open={Boolean(message)} autoHideDuration={4000} onClose={handleClose}>
      <Alert severity="success" onClose={handleClose} sx={{ width: '100%' }}>
        {message}
      </Alert>
    </Snackbar>
  );
}
