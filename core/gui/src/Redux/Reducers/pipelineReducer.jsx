import { pipelineConstants } from '../actions/pipelineActions/pipelineActions';
import { userConstants } from '../actions/userAuthActions/userAuthActions';

const INITIAL_STATE = {
  pipelines: [],
  oAuthToken: 'loading',
  expanded: false
};

const pipelineReducer = (state = INITIAL_STATE, action) => {
  const { RECEIVE_PIPELINES, REQUEST_PIPELINES } = pipelineConstants;
  const { STORE_USER_INFO } = userConstants;

  switch (action.type) {
    case STORE_USER_INFO:
      return Object.assign({}, state, {
        oAuthToken: action.oAuthToken
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
