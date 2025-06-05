import { combineReducers } from '@reduxjs/toolkit';
import cityReducer from '../components/Entities/City/citySlice.js';
import schoolReducer from '../components/Entities/School/schoolSlice.js';
import subjectReducer from '../components/Entities/Subject/subjectSlice.js';
// other reducers can be added here
import notificationReducer from './toastSlice.js';

export default combineReducers({
  cities: cityReducer,
  schools: schoolReducer,
  subjects: subjectReducer,
  notifications: notificationReducer,
});
