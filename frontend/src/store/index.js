// src/store/index.js
import { configureStore } from '@reduxjs/toolkit';
import gradebookReducer from './gradebookSlice';

const store = configureStore({
  reducer: {
    gradebooks: gradebookReducer,
  },
});

export default store;