// src/hooks/useGradebooks.js
import { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchGradebooks } from '../store/gradebookSlice';

export default function useGradebooks() {
  const dispatch = useDispatch();
  const { items, status, error } = useSelector(state => state.gradebooks);

  useEffect(() => {
    if (status === 'idle') {
      dispatch(fetchGradebooks());
    }
  }, [status, dispatch]);

  return { gradebooks: items, status, error };
}