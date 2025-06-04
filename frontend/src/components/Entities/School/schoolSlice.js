import { createSlice } from '@reduxjs/toolkit';

const slice = createSlice({
  name: 'schools',
  initialState: { items: [] },
  reducers: {
    setSchools(state, action) {
      state.items = action.payload;
    },
  },
});

export const { setSchools } = slice.actions;
export default slice.reducer;
