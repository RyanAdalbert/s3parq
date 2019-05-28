import { filtersConstants } from '../actions/filtersActions/filtersActions';

const INITIAL_STATE = {
  filters: []
};

const filtersReducer = (state = INITIAL_STATE, action) => {
  const {
    FETCH_FILTERS,
    FETCH_FILTERS_SUCCESS,
    FETCH_FILTERS_FAILURE
  } = filtersConstants;
  switch (action.type) {
    case FETCH_FILTERS:
      return Object.assign({}, state, {
        isFetching: true,
        didInvalidate: false
      });
    case FETCH_FILTERS_SUCCESS:
      return Object.assign({}, state, {
        isFetching: false,
        didInvalidate: false,
        filters: action.payload.data
      });
    case FETCH_FILTERS_FAILURE:
      return Object.assign({}, state, {
        isFetching: false,
        didInvalidate: true
      });
    default:
      return state;
  }
};

export default filtersReducer;
