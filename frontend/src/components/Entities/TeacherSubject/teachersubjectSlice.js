import { createSlice } from '@reduxjs/toolkit';

const slice = createSlice({
  name: 'teachersubjects',
  initialState: { items: [] },
  reducers: {
    setTeacherSubjects(state, action) {
      state.items = action.payload;
    },
  },
});

export const { setTeacherSubjects } = slice.actions;
export default slice.reducer;
