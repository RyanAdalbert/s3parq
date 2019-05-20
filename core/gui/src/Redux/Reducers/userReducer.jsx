import { userConstants } from '../actions/userAuthActions/userAuthActions';

export const INITIAL_STATE = {
  oAuthToken: 'loading',
  userName: 'loading',
  isLoggedIn: 'loading'
};

const userReducer = (state = INITIAL_STATE, action) => {
  const { LOGIN_ATTEMPT, LOGIN_SUCCESS } = userConstants;
  switch (action.type) {
    case LOGIN_ATTEMPT:
      return Object.assign({}, state, {
        isLoggingIn: true,
        isLoggedIn: false
      });
    case LOGIN_SUCCESS:
      return Object.assign({}, state, {
        error: null,
        isLoggingIn: false,
        isLoggedIn: true
      });
    default:
      return state;
  }
};

export default userReducer;
