import { createSlice } from '@reduxjs/toolkit';

const slice = createSlice({
  name: 'parents',
  initialState: { items: [] },
  reducers: {
    setParents(state, action) {
      state.items = action.payload;
    },
  },
});

export const { setParents } = slice.actions;
export default slice.reducer;
