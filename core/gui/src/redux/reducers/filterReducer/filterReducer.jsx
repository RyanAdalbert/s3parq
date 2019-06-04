import { filterConstants } from '../../actions/filterActions/filterActions';
import { combineReducers } from 'redux';

const FILTERS_STATE = {
  filters: []
};

const fetchFilters = (state = FILTERS_STATE, action) => {
  const {
    FETCH_FILTERS,
    FETCH_FILTERS_SUCCESS,
    FETCH_FILTERS_FAILURE
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
    default:
      return state;
  }
};

const SET_FILTERS_STATE = {
  setBrand: 'Brand',
  setCompany: 'Company',
  setStatus: 'Status'
};
//Reducer that handles selected filters so we can pass this object to our filter function
const setFilters = (state = SET_FILTERS_STATE, action) => {
  const {
    SET_FILTER_BRAND,
    SET_FILTER_COMPANY,
    SET_FILTER_STATUS
  } = filterConstants;

  switch (action.type) {
    case SET_FILTER_BRAND:
      return Object.assign({}, state, {
        setBrand: action.evt
      });
    case SET_FILTER_COMPANY:
      return Object.assign({}, state, {
        setCompany: action.evt
      });
    case SET_FILTER_STATUS:
      return Object.assign({}, state, {
        setStatus: action.evt
      });
    default:
      return state;
  }
};

export const filterReducer = combineReducers({ fetchFilters, setFilters });
