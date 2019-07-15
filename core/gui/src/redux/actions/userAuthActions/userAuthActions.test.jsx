import configureMockStore from 'redux-mock-store';
import thunk from 'redux-thunk';
import expect from 'expect'; // You can use any testing library
import fetchMock from 'fetch-mock';
import { userConstants } from './userAuthActions';
import * as actions from './userAuthActions';

import { API_HOST } from '../../constants';
const middlewares = [thunk];
const mockStore = configureMockStore(middlewares);

describe('Authorization results', () => {
  it('Login Attempt', () => {
    const oAuthToken = '9999999';
    const expectedAction = {
      type: userConstants.LOGIN_ATTEMPT,
      oAuthToken
    };
    expect(actions.loginAttempt(oAuthToken)).toEqual(expectedAction);
  });

  it('Login Success', () => {
    const status = undefined;

    const expectedAction = {
      type: userConstants.LOGIN_SUCCESS,
      status
    };

    let retnFunc = actions.loginSuccess();
    retnFunc(receivedAction => {
      expect(receivedAction).toEqual(expectedAction);
    });
  });

  it('Login Error', () => {
    const response = 'Error';
    const expectedAction = {
      type: userConstants.LOGIN_FAIL,
      response
    };
    expect(actions.loginError(response)).toEqual(expectedAction);
  });

  it('Stores the token', () => {
    const oAuthToken = '99999';
    const userName = 'Nova';

    const expectedAction = {
      type: userConstants.STORE_TOKEN,
      payload: {
        oAuthToken: oAuthToken,
        userName: userName
      }
    };
    expect(actions.storeToken(oAuthToken, userName)).toEqual(expectedAction);
  });
});

describe('Authorization', () => {
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
        status: { status: 200 }
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
