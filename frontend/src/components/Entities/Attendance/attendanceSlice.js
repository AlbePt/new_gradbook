import { createSlice } from '@reduxjs/toolkit';

const slice = createSlice({
  name: 'attendances',
  initialState: { items: [] },
  reducers: {
    setAttendances(state, action) {
      state.items = action.payload;
    },
  },
});

export const { setAttendances } = slice.actions;
export default slice.reducer;
