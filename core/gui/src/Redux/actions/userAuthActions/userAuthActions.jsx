import history from '../../../utils/history';

//User Constants
export const userConstants = {
  STORE_TOKEN: 'STORE_TOKEN',
  LOGIN_ATTEMPT: 'LOGIN_ATTEMPT',
  LOGIN_FAIL: 'LOGIN_FAIL',
  LOGIN_SUCCESS: 'LOGIN_SUCCESS',
  USER_LOGOUT: 'USER_LOGOUT'
};

export const loginRequest = oAuthToken => {
  return {
    type: 'LOGIN_ATTEMPT',
    oAuthToken
  };
};

// login flow action creators
export const loginError = error => {
  return {
    type: 'LOGIN_FAIL',
    error
  };
};

export const loginSuccess = response => {
  return dispatch => {
    dispatch({
      type: 'LOGIN_SUCCESS',
      response
    });
    history.push('/admin');
  };
};

// store token action creator
export const storeToken = (oAuthToken, userName) => ({
  type: 'STORE_TOKEN',
  payload: {
    oAuthToken,
    userName
  }
});

//login action creator
export const login = oAuthToken => {
  const HOST = 'localhost';
  return dispatch =>
    fetch(`http://${HOST}:5000/config_api/login`, {
      method: 'GET',
      headers: {
        Authorization: oAuthToken
      }
    })
      .then(response => {
        if (response.status === 200) {
          dispatch(loginSuccess(response));
        } else {
          const error = new Error(response.statusText);
          error.response = response;
          dispatch(loginError(error));
          throw error;
        }
      })
      .catch(error => {
        console.log('request failed', error);
      });
};

//logout action creator
export const logOut = () => {
  return {
    type: 'USER_LOGOUT'
  };
};
