import { pipelineConstants } from '../actions/pipelineActions/pipelineActions';
import { userConstants } from '../actions/userAuthActions/userAuthActions';

const INITIAL_STATE = {
  pipelines: [],
  oAuthToken: 'loading'
};

const pipelineReducer = (state = INITIAL_STATE, action) => {
  const { RECEIVE_PIPELINES, REQUEST_PIPELINES } = pipelineConstants;
  const { STORE_TOKEN } = userConstants;

  switch (action.type) {
    case STORE_TOKEN:
      return {
        state,
        oAuthToken: action.payload.oAuthToken
      };
    case REQUEST_PIPELINES:
      return {
        ...state,
        isFetching: true,
        didInvalidate: false
      };
    case RECEIVE_PIPELINES:
      return {
        ...state,
        isFetching: false,
        didInvalidate: false,
        items: action.pipelines,
        lastUpdated: action.receivedAt
      };
    default:
      return state;
  }
};

export default pipelineReducer;
