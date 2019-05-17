//Pipeline Constants
export const pipelineConstants = {
  REQUEST_PIPELINES: 'REQUEST_PIPELINES',
  RECEIVE_PIPELINES: 'RECEIVE_PIPELINES',
  EXPAND_DETAILS: 'EXPAND_DETAILS'
};

export const requestPipelines = pipelines => {
  return {
    type: 'REQUEST_PIPELINES',
    pipelines
  };
};

export const receivePipelines = json => {
  return {
    type: 'RECEIVE_PIPELINES',
    pipelines: json.data.map(pipeline => pipeline)
  };
};

export const fetchPipelines = oAuthToken => {
  const HOST = 'localhost';
  return dispatch => {
    return fetch(`http://${HOST}:5000/config_api/index`, {
      method: 'GET',
      headers: {
        Authorization: oAuthToken
      },
      credentials: 'include'
    })
      .then(response => response.json())
      .then(json => dispatch(receivePipelines(json)))
      .catch(error => {
        console.log('request failed', error);
      });
  };
};
