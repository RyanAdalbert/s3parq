import { userConstants } from '../../actions/userAuthActions/userAuthActions';

export const INITIAL_STATE = {
  oAuthToken: 'loading',
  userName: 'loading',
  isLoggedIn: 'loading'
};

const { LOGIN_ATTEMPT, LOGIN_SUCCESS, LOGIN_FAIL, STORE_TOKEN } = userConstants;

const userReducer = (state = INITIAL_STATE, action) => {
  switch (action.type) {
    case LOGIN_ATTEMPT:
      return Object.assign({}, state, {
        isLoggingIn: true,
        isLoggedIn: false
      });
    case LOGIN_FAIL:
      return Object.assign({}, state, {
        error: action.error,
        isLoggingIn: false,
        isLoggedIn: false
      });
    case LOGIN_SUCCESS:
      return Object.assign({}, state, {
        error: null,
        isLoggingIn: false,
        isLoggedIn: true
      });
    case STORE_TOKEN:
      const { oAuthToken, userName } = action.payload;
      return Object.assign({}, state, {
        oAuthToken,
        userName
      });
    default:
      return state;
  }
};

export default userReducer;