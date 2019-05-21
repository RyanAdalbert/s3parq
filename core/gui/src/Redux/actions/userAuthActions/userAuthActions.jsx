import history from '../../../utils/history';

//User Constants
export const userConstants = {
  LOGIN_ATTEMPT: 'LOGIN_ATTEMPT',
  LOGIN_SUCCESS: 'LOGIN_SUCCESS',
  LOGIN_FAILURE: 'LOGIN_FAILURE',
  STORE_USER_INFO: 'STORE_USER_INFO',
  USER_LOGOUT: 'USER_LOGOUT'
};

// login flow action creators
export const loginError = error => ({
  type: 'LOGIN_FAILURE',
  error
});

export const loginSuccess = response => {
  return dispatch => {
    dispatch({
      type: 'LOGIN_SUCCESS',
      response
    });
    history.push('/admin/pipelineindex');
  };
};

export const userAuth = (oAuthToken, userName) => ({
  type: 'LOGIN_ATTEMPT',
  config: {
    endPoint: `/config_api/login`,
    method: 'GET',
    headers: {
      authorization: oAuthToken
    },
    credentials: 'include',
    userName
  }
});

export const storeUserInfo = (oAuthToken, userName) => ({
  type: 'STORE_USER_INFO',
  oAuthToken,
  userName
});

//logout action creator
export const logOut = () => ({
  type: 'USER_LOGOUT'
});
