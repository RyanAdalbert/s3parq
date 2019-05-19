import { userConstants } from '../actions/userAuthActions/userAuthActions';

export const INITIAL_STATE = {
  oAuthToken: 'loading',
  userName: 'loading',
  isLoggedIn: 'loading'
};

const userReducer = (state = INITIAL_STATE, action) => {
  const { USER_AUTH } = userConstants;
  switch (action.type) {
    case USER_AUTH:
      return Object.assign({}, state, {
        isLoggingIn: true,
        isLoggedIn: false
      });
    default:
      return state;
  }
};

export default userReducer;
