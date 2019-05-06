import { userConstants } from '../actions/userAuthActions';

export const INITIAL_STATE = {
  oAuthToken: '',
  userName: ''
};

const { LOGIN_ATTEMPT, LOGIN_SUCCESS, LOGIN_FAIL, STORE_TOKEN } = userConstants;

const userReducer = (state = INITIAL_STATE, action) => {
  switch (action.type) {
    case LOGIN_ATTEMPT:
      return {
        isLoggingIn: true,
        isLoggedIn: false
      };
    case LOGIN_FAIL:
      return {
        error: action.error,
        isLoggingIn: false,
        isLoggedIn: false
      };
    case LOGIN_SUCCESS:
      return {
        state,
        error: null,
        isLoggingIn: false,
        isLoggedIn: true
      };
    case STORE_TOKEN:
      const { oAuthToken, userName } = action.payload;
      return {
        state,
        oAuthToken,
        userName
      };
    default:
      return state;
  }
};

export default userReducer;
