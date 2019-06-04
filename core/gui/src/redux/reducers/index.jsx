import { combineReducers } from 'redux';
import userReducer from './userReducer/userReducer';
import pipelineReducer from './pipelineReducer/pipelineReducer';
import { filterReducer } from './filterReducer/filterReducer';

const appReducer = combineReducers({
  userReducer,
  pipelineReducer,
  filterReducer
});

const rootReducer = (state, action) => {
  if (action.type === 'USER_LOGOUT') {
    state = undefined;
  }

  return appReducer(state, action);
};

export default rootReducer;
