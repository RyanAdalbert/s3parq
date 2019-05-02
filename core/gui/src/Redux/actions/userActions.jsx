import history from '../../utils/history';

//User Constants
export const userConstants = {
  STORE_TOKEN: 'STORE_TOKEN',
  LOGIN_ATTEMPT: 'LOGIN_ATTEMPT',
  LOGIN_FAIL: 'LOGIN_FAIL',
  LOGIN_SUCCESS: 'LOGIN_SUCCESS'
};

// store token action creator
export const storeToken = (oAuthToken, userName) => ({
  type: 'STORE_TOKEN',
  payload: {
    oAuthToken,
    userName
  }
});

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

export const loginRequest = oAuthToken => {
  return {
    type: 'LOGIN_ATTEMPT',
    oAuthToken
  };
};

//login action creator
export const login = userData => {
  return dispatch =>
    fetch(
      `http://core_flaskapi_1/${
        process.env.REACT_APP_ICHAIN_API_HOST
      }/5000/config_api/login`,
      {
        method: 'post',
        headers: {
          Authorization: userData.oAuthToken
        },
        body: JSON.stringify({
          token: userData.oAuthToken
        })
      }
    )
      .then(response => {
        if (response.status === 200) {
          console.log(response);
          dispatch(loginSuccess(response));
          dispatch(storeToken(userData.oAuthToken, userData.userName));
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
