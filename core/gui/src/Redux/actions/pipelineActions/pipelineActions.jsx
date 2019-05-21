//Pipeline Constants
export const pipelineConstants = {
  REQUEST_PIPELINES: 'REQUEST_PIPELINES',
  RECEIVE_PIPELINES: 'RECEIVE_PIPELINES',
  EXPAND_DETAILS: 'EXPAND_DETAILS'
};

export const receivePipelines = json => {
  return {
    type: 'RECEIVE_PIPELINES',
    pipelines: json.data.map(pipeline => pipeline)
  };
};

export const fetchPipelines = oAuthToken => ({
  type: 'REQUEST_PIPELINES',
  config: {
    endPoint: `/config_api/index`,
    method: 'GET',
    headers: {
      authorization: oAuthToken
    },
    credentials: 'include'
  }
});
