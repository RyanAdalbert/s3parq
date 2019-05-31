import { filterConstants } from '../../actions/filterActions/filterActions';

const INITIAL_STATE = {
  filters: [],
  brand: 'brand',
  company: 'company',
  type: 'type',
  status: 'status'
};

const filterReducer = (state = INITIAL_STATE, action) => {
  const {
    FETCH_FILTERS,
    FETCH_FILTERS_SUCCESS,
    FETCH_FILTERS_FAILURE,
    SET_FILTER_BRAND,
    SET_FILTER_COMPANY,
    SET_FILTER_TYPE,
    SET_FILTER_STATUS
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
    case SET_FILTER_BRAND:
      return Object.assign({}, state, {
        brand: action.evt
      });
    case SET_FILTER_COMPANY:
      return Object.assign({}, state, {
        company: action.evt
      });
    case SET_FILTER_TYPE:
      return Object.assign({}, state, {
        type: action.evt
      });
    case SET_FILTER_STATUS:
      return Object.assign({}, state, {
        status: action.evt
      });
    default:
      return state;
  }
};

export default filterReducer;
