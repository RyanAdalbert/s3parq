const API_ROOT = 'http://localhost:5000';

const fetchMiddleware = store => next => action => {
  if (!action || !action.fetchConfig) {
    return next(action);
  }

  let dispatch = store.dispatch;
  let config = action.fetchConfig;
  dispatch(config.init);

  const path = `${API_ROOT + config.path}`;
  const method = config.method || 'GET';
  const headers = config.headers;
  const credentials = config.credentials;
  const body = config.body;
  const successHandler = config.success;
  const failureHandler = config.failure;

  fetch(path, {
    method,
    headers,
    credentials,
    body: JSON.stringify(body)
  })
    .then(response => response.json())
    .then(json => console.log(json))
    .then(json => successHandler(json))
    .catch(error => failureHandler(error));
};

export default fetchMiddleware;
