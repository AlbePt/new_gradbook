import { createSlice } from '@reduxjs/toolkit';

const slice = createSlice({
  name: 'regions',
  initialState: { items: [] },
  reducers: {
    setRegions(state, action) {
      state.items = action.payload;
    },
  },
});

export const { setRegions } = slice.actions;
export default slice.reducer;
