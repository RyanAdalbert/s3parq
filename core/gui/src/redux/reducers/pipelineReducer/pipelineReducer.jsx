import { pipelineConstants } from '../../actions/pipelineActions/pipelineActions';

const INITIAL_STATE = {
  pipelines: [],
  modalShow: false,
  modalProps: {}
};

const pipelineReducer = (state = INITIAL_STATE, action) => {
  const {
    FETCH_PIPELINES,
    FETCH_PIPELINES_SUCCESS,
    FETCH_PIPELINES_FAILURE,
    MODAL_OPEN,
    MODAL_CLOSE
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
        pipelines: action.payload
      });
    case FETCH_PIPELINES_FAILURE:
      return Object.assign({}, state, {
        isFetching: false,
        fetched: false,
        didInvalidate: true
      });
    case MODAL_OPEN:
      return Object.assign({}, state, {
        modalShow: action.modalStatus,
        modalProps: action.modalProps
      });
    case MODAL_CLOSE:
      return Object.assign({}, state, {
        modalShow: action.modalStatus,
        modalProps: action.modalProps
      });
    default:
      return state;
  }
};

export default pipelineReducer;
