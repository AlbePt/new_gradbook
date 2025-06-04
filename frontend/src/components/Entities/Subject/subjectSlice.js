import { createSlice } from '@reduxjs/toolkit';

const slice = createSlice({
  name: 'subjects',
  initialState: { items: [] },
  reducers: {
    setSubjects(state, action) {
      state.items = action.payload;
    },
  },
});

export const { setSubjects } = slice.actions;
export default slice.reducer;
