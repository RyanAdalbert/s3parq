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
  SET_FILTER: 'SET_FILTER'
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

export const setFilter = evt => ({
  type: 'SET_FILTER',
  evt
});
