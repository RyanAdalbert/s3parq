//User Constants
export const userConstants = {
  GOOGLE_RESPONSE_SUCCESS: 'GOOGLE_RESPONSE_SUCCESS',
  LOGIN_REQUEST: 'LOGIN_REQUEST',
  LOGIN_SUCCESS: 'LOGIN_SUCCESS',
  LOGIN_FAILUER: 'LOGIN_FAILUER'
};

//Google Response Action
export const googleResponseSuccess = (oAuthToken, refreshToken, userName) => ({
  type: 'GOOGLE_RESPONSE_SUCCESS',
  payload: {
    oAuthToken,
    refreshToken,
    userName
  }
});

//User Auth Actions
