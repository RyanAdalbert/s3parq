import { userConstants } from '../actions/userActions';

export const INITIAL_STATE = {
  oAuthToken: '',
  refreshToken: '',
  userName: ''
};

const { LOGIN_ATTEMPT, LOGIN_SUCCESS, LOGIN_FAIL } = userConstants;

const userReducer = (state = INITIAL_STATE, action) => {
  switch (action.type) {
    // case userConstants.GOOGLE_RESPONSE_SUCCESS:
    //   const { oAuthToken, refreshToken, userName } = action.payload;
    //   return {
    //     state,
    //     oAuthToken,
    //     refreshToken,
    //     userName
    //   };
    case LOGIN_ATTEMPT:
      return state.merge({
        isLoggingIn: true,
        isLoggedIn: false
      });
    case LOGIN_FAIL:
      return state.merge({
        error: action.error,
        isLoggingIn: false,
        isLoggedIn: false
      });
    case LOGIN_SUCCESS:
      return state.merge({
        error: null,
        isLoggingIn: false,
        isLoggedIn: true
      });
    default:
      return state;
  }
};

export default userReducer;
