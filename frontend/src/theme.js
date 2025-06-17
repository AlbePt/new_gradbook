import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: { main: '#3B82F6' },
    secondary: { main: '#22C55E' },
    error: { main: '#EF4444' },
    background: { default: '#F7F7F7' },
    text: { primary: '#111827' }
  },
  typography: {
    fontFamily: 'Inter, sans-serif',
    fontSize: 14,
    h6: { fontSize: 20, fontWeight: 600 },
    h5: { fontSize: 24, fontWeight: 700 }
  },
  shape: { borderRadius: 8 },
  shadows: [
    'none',
    '0px 4px 10px rgba(0,0,0,0.08)',
    ...Array(23).fill('none')
  ],
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          boxShadow: 'none'
        }
      }
    }
  }
});

export default theme;
