import { createSlice } from '@reduxjs/toolkit';

const slice = createSlice({
  name: 'classs',
  initialState: { items: [] },
  reducers: {
    setClasss(state, action) {
      state.items = action.payload;
    },
  },
});

export const { setClasss } = slice.actions;
export default slice.reducer;
