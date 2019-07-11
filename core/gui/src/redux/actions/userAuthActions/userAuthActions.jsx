import history from '../../../utils/history';
import { API_HOST } from '../../constants.jsx';

//User Constants
export const userConstants = {
  STORE_TOKEN: 'STORE_TOKEN',
  LOGIN_ATTEMPT: 'LOGIN_ATTEMPT',
  LOGIN_FAIL: 'LOGIN_FAIL',
  LOGIN_SUCCESS: 'LOGIN_SUCCESS',
  USER_LOGOUT: 'USER_LOGOUT'
};

export const loginAttempt = oAuthToken => {
  return {
    type: 'LOGIN_ATTEMPT',
    oAuthToken
  };
};

// login flow action creators
export const loginError = response => {
  return {
    type: 'LOGIN_FAIL',
    response
  };
};

export const loginSuccess = status => {
  return dispatch => {
    dispatch({
      type: 'LOGIN_SUCCESS',
      status
    });
    history.push('/admin/pipelineindex');
  };
};

// store token action creator
export const storeToken = userInfo => ({
  type: 'STORE_TOKEN',
  payload: {
    oAuthToken: userInfo.oAuthToken,
    userName: userInfo.userName
  }
});

//login action creator
export const login = oAuthToken => {
  return dispatch => {
    return fetch(`${API_HOST}/config_api/login`, {
      method: 'GET',
      headers: {
        Authorization: oAuthToken
      },
      credentials: 'include'
    })
      .then(response => {
        if (response.status === 200) {
          dispatch(loginSuccess({ status: response.status }));
        } else {
          dispatch(loginError({ status: response.status }));
          const error = new Error(response.statusText);
          throw error;
        }
      })
      .catch(error => {
        console.log('request failed', error);
      });
  };
};

//logout action creator
export const logOut = () => ({
  type: 'USER_LOGOUT'
});
