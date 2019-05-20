import history from '../../../utils/history';

//User Constants
export const userConstants = {
  LOGIN_ATTEMPT: 'LOGIN_ATTEMPT',
  LOGIN_SUCCESS: 'LOGIN_SUCCESS',
  LOGIN_FAILURE: 'LOGIN_FAILURE',
  USER_LOGOUT: 'USER_LOGOUT'
};

// login flow action creators
export const loginError = error => {
  return {
    type: 'LOGIN_FAILURE',
    error
  };
};

export const loginSuccess = response => {
  return dispatch => {
    dispatch({
      type: 'LOGIN_SUCCESS',
      response
    });
    history.push('/admin/pipelineindex');
  };
};

export const userAuth = oAuthToken => ({
  type: 'LOGIN_ATTEMPT',
  config: {
    endPoint: `/config_api/login`,
    method: 'GET',
    headers: {
      authorization: oAuthToken
    },
    credentials: 'include'
  }
});

//logout action creator
export const logOut = () => {
  return {
    type: 'USER_LOGOUT'
  };
};
