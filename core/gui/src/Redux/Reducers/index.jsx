import { combineReducers } from 'redux';
import userReducer from './userReducer';
import pipelineReducer from './pipelineReducer';
import filtersReducer from './filtersReducer';

const appReducer = combineReducers({
  userReducer,
  pipelineReducer,
  filtersReducer
});

const rootReducer = (state, action) => {
  if (action.type === 'USER_LOGOUT') {
    state = undefined;
  }

  return appReducer(state, action);
};

export default rootReducer;
