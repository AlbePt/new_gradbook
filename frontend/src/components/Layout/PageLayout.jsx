import React from 'react';
import { AppBar, Toolbar, Container, Box, Typography } from '@mui/material';

export default function PageLayout({ children }) {
  return (
    <>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            ЭЖ
          </Typography>
        </Toolbar>
      </AppBar>
      <Container component="main" sx={{ my: 4 }}>
        {children}
      </Container>
      <Box component="footer" sx={{ p: 2, textAlign: 'center', bgcolor: 'background.default' }}>
        <Typography variant="body2">© 2024</Typography>
      </Box>
    </>
  );
}
