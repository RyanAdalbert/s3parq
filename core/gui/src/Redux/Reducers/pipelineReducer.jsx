import { pipelineConstants } from '../actions/pipelineActions/pipelineActions';

const INITIAL_STATE = {
  pipelines: []
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
        fetched: false,
        didInvalidate: false
      });
    case FETCH_PIPELINES_SUCCESS:
      return Object.assign({}, state, {
        isFetching: false,
        fetched: true,
        didInvalidate: false,
        pipelines: action.payload.data
      });
    case FETCH_PIPELINES_FAILURE:
      return Object.assign({}, state, {
        isFetching: false,
        fetched: false,
        didInvalidate: true
      });
    default:
      return state;
  }
};

export default pipelineReducer;
