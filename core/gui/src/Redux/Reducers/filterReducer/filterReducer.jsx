import { filterConstants } from '../../actions/filterActions/filterActions';

const INITIAL_STATE = {
  filters: [],
  setFilters: {}
};

const filterReducer = (state = INITIAL_STATE, action) => {
  const {
    FETCH_FILTERS,
    FETCH_FILTERS_SUCCESS,
    FETCH_FILTERS_FAILURE,
    SET_FILTER
  } = filterConstants;
  switch (action.type) {
    case FETCH_FILTERS:
      return Object.assign({}, state, {
        isFetching: true,
        didInvalidate: false,
        fetched: false
      });
    case FETCH_FILTERS_SUCCESS:
      return Object.assign({}, state, {
        isFetching: false,
        didInvalidate: false,
        filters: action.payload.data,
        fetched: true
      });
    case FETCH_FILTERS_FAILURE:
      return Object.assign({}, state, {
        isFetching: false,
        didInvalidate: true,
        fetched: false
      });
    case SET_FILTER:
      return Object.assign({}, state, {
        setFilters: action.evt
      });
    default:
      return state;
  }
};

export default filterReducer;
