import { combineReducers } from 'redux';
import userReducer from './userReducer';
import pipelineReducer from './pipelineReducer';

const appReducer = combineReducers({
  userReducer,
  pipelineReducer
});

const rootReducer = (state, action) => {
  if (action.type === 'USER_LOGOUT') {
    state = undefined;
  }

  return appReducer(state, action);
};

export default rootReducer;
