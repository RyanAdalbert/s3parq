import { userConstants } from '../actions/userActions';

export const INITIAL_STATE = {
  oAuthToken: '',
  refreshToken: '',
  userName: ''
};

const userReducer = (state = INITIAL_STATE, action) => {
  switch (action.type) {
    case userConstants.GOOGLE_RESPONSE_SUCCESS:
      const { oAuthToken, refreshToken, userName } = action.payload;
      return {
        state,
        oAuthToken,
        refreshToken,
        userName
      };
    default:
      return state;
  }
};

export default userReducer;
