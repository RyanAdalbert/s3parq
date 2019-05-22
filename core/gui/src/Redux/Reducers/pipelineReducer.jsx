import { pipelineConstants } from '../actions/pipelineActions/pipelineActions';

const INITIAL_STATE = {
  pipelines: [],
  expanded: false
};

const pipelineReducer = (state = INITIAL_STATE, action) => {
  const {
    FETCH_PIPELINES,
    FETCH_PIPELINES_SUCCESS,
    FETCH_PIPELINES_FAILURE
  } = pipelineConstants;
  switch (action.type) {
    case FETCH_PIPELINES:
      return Object.assign({}, state, {
        isFetching: true,
        didInvalidate: false
      });
    case FETCH_PIPELINES_SUCCESS:
      return Object.assign({}, state, {
        isFetching: false,
        didInvalidate: false,
        pipelines: action.payload.data
      });
    case FETCH_PIPELINES_FAILURE:
      return Object.assign({}, state, {
        isFetching: false,
        didInvalidate: true
      });
    default:
      return state;
  }
};

export default pipelineReducer;
