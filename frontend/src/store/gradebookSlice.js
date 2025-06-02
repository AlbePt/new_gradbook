// src/store/gradebookSlice.js
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getGradebooks,
  getGradebook,
  createGradebook,
  updateGradebook,
  deleteGradebook,
} from '../api/gradebookApi';

// Async actions
export const fetchGradebooks = createAsyncThunk(
  'gradebooks/fetchAll',
  async (_, { rejectWithValue }) => {
    try {
      const response = await getGradebooks();
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response.data);
    }
  }
);

export const fetchGradebookById = createAsyncThunk(
  'gradebooks/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      const response = await getGradebook(id);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response.data);
    }
  }
);

export const addGradebook = createAsyncThunk(
  'gradebooks/add',
  async (data, { rejectWithValue }) => {
    try {
      const response = await createGradebook(data);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response.data);
    }
  }
);

export const editGradebook = createAsyncThunk(
  'gradebooks/edit',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      const response = await updateGradebook(id, data);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response.data);
    }
  }
);

export const removeGradebook = createAsyncThunk(
  'gradebooks/remove',
  async (id, { rejectWithValue }) => {
    try {
      await deleteGradebook(id);
      return id;
    } catch (error) {
      return rejectWithValue(error.response.data);
    }
  }
);

const initialState = {
  items: [],
  current: null,
  status: 'idle', // 'idle' | 'loading' | 'succeeded' | 'failed'
  error: null,
};

const gradebookSlice = createSlice({
  name: 'gradebooks',
  initialState,
  reducers: {
    clearError: (state) => {
      state.status = 'idle';
      state.error = null;
    },
    resetCurrent: (state) => {
      state.current = null;
    }
  },
  extraReducers: (builder) => {
    builder
      // Конкретные обработчики fulfilled
      .addCase(fetchGradebooks.fulfilled, (state, action) => {
        state.status = 'succeeded';
        state.items = action.payload;
      })
      .addCase(fetchGradebookById.fulfilled, (state, action) => {
        state.status = 'succeeded';
        state.current = action.payload;
      })
      .addCase(addGradebook.fulfilled, (state, action) => {
        state.items.push(action.payload);
        state.status = 'succeeded';
      })
      .addCase(editGradebook.fulfilled, (state, action) => {
        const index = state.items.findIndex(gb => gb.id === action.payload.id);
        if (index !== -1) state.items[index] = action.payload;
        if (state.current?.id === action.payload.id) state.current = action.payload;
        state.status = 'succeeded';
      })
      .addCase(removeGradebook.fulfilled, (state, action) => {
        state.items = state.items.filter(gb => gb.id !== action.payload);
        if (state.current?.id === action.payload) state.current = null;
        state.status = 'succeeded';
      })

      // Общие обработчики состояний
      .addMatcher(
        (action) => action.type.endsWith('/pending'),
        (state) => {
          state.status = 'loading';
          state.error = null;
        }
      )
      .addMatcher(
        (action) => action.type.endsWith('/rejected'),
        (state, action) => {
          state.status = 'failed';
          state.error = action.payload?.message || action.error.message;
        }
      );
  },
});

export const { clearError, resetCurrent } = gradebookSlice.actions;
export default gradebookSlice.reducer;