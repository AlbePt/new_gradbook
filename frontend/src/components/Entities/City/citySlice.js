import { createSlice } from '@reduxjs/toolkit';

const slice = createSlice({
  name: 'cities',
  initialState: { items: [] },
  reducers: {
    setCities(state, action) {
      state.items = action.payload;
    },
  },
});

export const { setCities } = slice.actions;
export default slice.reducer;
