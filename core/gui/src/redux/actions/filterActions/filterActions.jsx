import { RSAA } from 'redux-api-middleware';
import { API_HOST } from '../../constants';

export const setVisibilityFilter = filter => ({
  type: 'SET_VISIBILITY_FILTER',
  filter
});

//Filters Constants
export const filterConstants = {
  FETCH_FILTERS: 'FETCH_FILTERS',
  FETCH_FILTERS_SUCCESS: 'FETCH_FILTERS_SUCCESS',
  FETCH_FILTERS_FAILURE: 'FETCH_FILTERS_FAILURE',
  SET_FILTER_BRAND: 'SET_FILTER_BRAND',
  SET_FILTER_COMPANY: 'SET_FILTER_COMPANY',
  SET_FILTER_TYPE: 'SET_FILTER_TYPE',
  SET_FILTER_STATUS: 'SET_FILTER_STATUS'
};

//Fetch Filters with redux-api-middleware
export const fetchFilters = oAuthToken => ({
  //The parameters of the API call are specified by root properties of the [RSAA] property of an RSAA.
  [RSAA]: {
    endpoint: `${API_HOST}/config_api/filters`,
    method: 'GET',
    headers: {
      authorization: oAuthToken
    },
    credentials: 'include',
    types: [
      'FETCH_FILTERS',
      {
        type: 'FETCH_FILTERS_SUCCESS',
        payload: (action, state, res) => {
          return res.json();
        }
      },
      'FETCH_FILTERS_FAILURE'
    ]
  }
});

export const setFilterBrand = evt => ({
  type: 'SET_FILTER_BRAND',
  evt
});

export const setFilterCompany = evt => ({
  type: 'SET_FILTER_COMPANY',
  evt
});

export const setFilterType = evt => ({
  type: 'SET_FILTER_TYPE',
  evt
});

export const setFilterStatus = evt => ({
  type: 'SET_FILTER_STATUS',
  evt
});
