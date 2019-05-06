import { combineReducers } from 'redux';
import userReducer from './userReducer';

const appReducer = combineReducers({
  userReducer
});

const rootReducer = (state, action) => {
  if (action.type === 'USER_LOGOUT') {
    state = undefined;
  }

  return appReducer(state, action);
};

export default rootReducer;
