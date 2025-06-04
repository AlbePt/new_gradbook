import { createSlice } from '@reduxjs/toolkit';

const slice = createSlice({
  name: 'grades',
  initialState: { items: [] },
  reducers: {
    setGrades(state, action) {
      state.items = action.payload;
    },
  },
});

export const { setGrades } = slice.actions;
export default slice.reducer;
