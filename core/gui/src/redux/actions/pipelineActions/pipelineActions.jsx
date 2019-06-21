import { RSAA } from 'redux-api-middleware';
import { API_HOST } from '../../constants';

//Pipeline Constants
export const pipelineConstants = {
  FETCH_PIPELINES: 'FETCH_PIPELINES',
  FETCH_PIPELINES_SUCCESS: 'FETCH_PIPELINES_SUCCESS',
  FETCH_PIPELINE_FAILURE: 'FETCH_PIPELINES_FAILURE',
  MODAL_OPEN: 'MODAL_OPEN',
  MODAL_CLOSE: 'MODAL_CLOSE'
};

//Fetch Pipeline with redux-api-middleware
export const fetchPipelines = oAuthToken => ({
  //The parameters of the API call are specified by root properties of the [RSAA] property of an RSAA.
  [RSAA]: {
    endpoint: `${API_HOST}/config_api/index`,
    method: 'GET',
    headers: {
      authorization: oAuthToken
    },
    credentials: 'include',
    types: [
      'FETCH_PIPELINES',
      {
        type: 'FETCH_PIPELINES_SUCCESS',
        payload: (action, state, res) => {
          return res.json();
        }
      },
      'FETCH_PIPELINES_FAILURE'
    ]
  }
});

export const modalOpen = (modalStatus, modalProps) => ({
  type: 'MODAL_OPEN',
  modalStatus,
  modalProps
});

export const modalClose = (modalStatus, modalProps) => ({
  type: 'MODAL_CLOSE',
  modalStatus,
  modalProps
});
