import { pipelineConstants } from '../actions/pipelineActions/pipelineActions';
import { userConstants } from '../actions/userAuthActions/userAuthActions';

const INITIAL_STATE = {
  pipelines: [],
  oAuthToken: 'loading',
  expanded: false
};

const pipelineReducer = (state = INITIAL_STATE, action) => {
  const { RECEIVE_PIPELINES, REQUEST_PIPELINES } = pipelineConstants;
  const { STORE_TOKEN } = userConstants;

  switch (action.type) {
    case STORE_TOKEN:
      return Object.assign({}, state, {
        oAuthToken: action.payload.oAuthToken
      });
    case REQUEST_PIPELINES:
      return Object.assign({}, state, {
        isFetching: true,
        didInvalidate: false
      });
    case RECEIVE_PIPELINES:
      return Object.assign({}, state, {
        isFetching: false,
        didInvalidate: false,
        pipelines: action.pipelines,
        lastUpdated: action.receivedAt
      });
    default:
      return state;
  }
};

export default pipelineReducer;
