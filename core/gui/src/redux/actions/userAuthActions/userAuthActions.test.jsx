import configureMockStore from 'redux-mock-store';
import thunk from 'redux-thunk';
import expect from 'expect'; // You can use any testing library
import fetchMock from 'fetch-mock';
import { userConstants } from './userAuthActions';
import * as actions from './userAuthActions';

import { API_HOST } from '../../constants';
const middlewares = [thunk];
const mockStore = configureMockStore(middlewares);

describe('Loging In', () => {
  afterEach(() => {
    fetchMock.restore();
  });

  it('creates LOGIN_SUCCESS action when response is status 200', () => {
    fetchMock.getOnce(`${API_HOST}/config_api/login`, {
      body: { status: 200 },
      headers: { 'content-type': 'application/json' }
    });

    const expectedActions = [
      {
        type: userConstants.LOGIN_ATTEMPT,
        type: userConstants.LOGIN_SUCCESS,
        response: { status: 200 }
      }
    ];

    const store = mockStore({ status: null });

    return store.dispatch(actions.login()).then(() => {
      // return of async actions
      expect(store.getActions()).toEqual(expectedActions);
    });
  });

  it('creates LOGIN_FAIL action when response is not status 200', () => {
    fetchMock.getOnce(`${API_HOST}/config_api/login`, {
      status: 403,
      headers: { 'content-type': 'application/json' }
    });

    const expectedActions = [
      {
        type: userConstants.LOGIN_ATTEMPT,
        type: userConstants.LOGIN_FAIL,
        response: { status: 403 }
      }
    ];

    const store = mockStore({ status: null });

    return store.dispatch(actions.login()).then(() => {
      // return of async actions
      expect(store.getActions()).toEqual(expectedActions);
    });
  });
});
