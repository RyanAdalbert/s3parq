//login action creator

export const CALL_API = 'Call API';

export const middleware = store => next => action => {
  const callAPI = action[CALL_API];

  if (typeof callAPI === 'undefined') {
    return next(action);
  }

  const { config } = action.config;

  const apiRoot = 'http://localhost:5000';
  const endPoint = config.endpoint;
  const headers = config.headers;
  const credentials = config.credentials;
  const method = config.method;

  return dispatch =>
    fetch(`${apiRoot}${endPoint}`, {
      method,
      headers,
      credentials
    })
      .then(response => {
        if (response.status === 200) {
          console.log('success');
        }
      })
      .catch(error => {
        console.log('request failed', error);
      });
};

export default middleware;
