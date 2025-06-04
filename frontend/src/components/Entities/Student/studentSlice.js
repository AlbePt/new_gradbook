import { createSlice } from '@reduxjs/toolkit';

const slice = createSlice({
  name: 'students',
  initialState: { items: [] },
  reducers: {
    setStudents(state, action) {
      state.items = action.payload;
    },
  },
});

export const { setStudents } = slice.actions;
export default slice.reducer;
