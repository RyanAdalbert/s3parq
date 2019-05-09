//Pipeline Constants
export const pipelineConstants = {
  REQUEST_PIPELINES: 'REQUEST_PIPELINES',
  RECEIVE_PIPELINES: 'RECEIVE_PIPELINES'
};

export const requestPipelines = pipelines => {
  return {
    type: 'REQUEST_PIPELINES',
    pipelines
  };
};

export const receivePipelines = json => {
  return {
    type: 'RECEIVE_POSTS',
    pipelines: JSON.data
  };
};

export const fetchPipelines = oAuthToken => {
  const HOST = 'localhost';
  return dispatch => {
    console.log(oAuthToken);
    fetch(`http://${HOST}:5000/config_api/index`, {
      method: 'GET',
      headers: {
        Authorization: oAuthToken
      }
    })
      .then(response => {
        console.log(response);
      })
      .catch(error => {
        console.log('request failed', error);
      });
  };
};
