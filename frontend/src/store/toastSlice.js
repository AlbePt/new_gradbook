import { createSlice } from '@reduxjs/toolkit';

const slice = createSlice({
  name: 'notifications',
  initialState: { items: [] },
  reducers: {
    addToast(state, action) {
      state.items.push({ id: Date.now(), ...action.payload });
    },
    removeToast(state, action) {
      state.items = state.items.filter(t => t.id !== action.payload);
    },
  },
});

export const { addToast, removeToast } = slice.actions;
export default slice.reducer;
