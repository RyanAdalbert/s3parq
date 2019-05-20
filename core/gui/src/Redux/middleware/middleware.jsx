import {
  loginSuccess,
  loginError
} from '../actions/userAuthActions/userAuthActions';

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

  return fetch(`${API_ROOT + END_POINT}`, {
    method,
    headers,
    credentials
  })
    .then(response => {
      if (response.status === 200) {
        console.log(response);
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

export default callApi;
