import { createSlice } from '@reduxjs/toolkit';

const slice = createSlice({
  name: 'academicyears',
  initialState: { items: [] },
  reducers: {
    setAcademicYears(state, action) {
      state.items = action.payload;
    },
  },
});

export const { setAcademicYears } = slice.actions;
export default slice.reducer;
