import * as actions from './userAuthActions';
import configureMockStore from 'redux-mock-store';
import thunk from 'redux-thunk';
import fetchMock from 'fetch-mock';

import { userConstants } from './userAuthActions';

const middlewares = [thunk];
const mockStore = configureMockStore(middlewares);

describe('action creators', () => {
  it('should create LOGIN_SUCCESS when loging in', () => {
    fetchMock.mock(`path:/config_api/login`, mockResult);

    const expectedActions = [
      { type: userConstants.LOGIN_ATTEMPT },
      { type: userConstants.LOGIN_SUCCESS, response: mockResult.body }
    ];

    const store = mockStore({
      search: {
        result: {}
      }
    });

    return store.dispatch(actions.login()).then(data => {
      // return of async actions
      expect(store.getActions()).toEqual(expectedActions);
    });
  });
});

describe('Logout Action', () => {
  it('should create an action to log the user out of the gui', () => {
    const expectedAction = {
      type: userConstants.USER_LOGOUT
    };
    expect(actions.logOut()).toEqual(expectedAction);
  });
});
