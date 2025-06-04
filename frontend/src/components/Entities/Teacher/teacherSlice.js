import { createSlice } from '@reduxjs/toolkit';

const slice = createSlice({
  name: 'teachers',
  initialState: { items: [] },
  reducers: {
    setTeachers(state, action) {
      state.items = action.payload;
    },
  },
});

export const { setTeachers } = slice.actions;
export default slice.reducer;
