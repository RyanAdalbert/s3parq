import {
  loginSuccess,
  loginError,
  storeUserInfo
} from '../actions/userAuthActions/userAuthActions';
import { receivePipelines } from '../actions/pipelineActions/pipelineActions';

//login action creator

export const CALL_API = 'Call API';
const API_ROOT = 'http://localhost:5000';

const callApi = store => next => action => {
  if (!action || !action.config) {
    return next(action);
  }

  let dispatch = store.dispatch;
  let config = action.config;

  const headers = config.headers;
  const credentials = config.credentials;
  const method = config.method;
  const END_POINT = config.endPoint;
  const userName = config.userName;

  localStorage.setItem('oAuthToken', headers.authorization);
  localStorage.setItem('userName', userName);

  if (action.type === 'LOGIN_ATTEMPT') {
    return fetch(`${API_ROOT + END_POINT}`, {
      method,
      headers,
      credentials
    })
      .then(response => {
        if (response.status === 200) {
          dispatch(storeUserInfo(headers.authorization, userName));
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
  } else {
    return fetch(`${API_ROOT + END_POINT}`, {
      method,
      headers,
      credentials
    })
      .then(response => response.json())
      .then(json => dispatch(receivePipelines(json)))
      .catch(error => {
        console.log('request failed', error);
      });
  }
};

export default callApi;
