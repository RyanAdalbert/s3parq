import configureMockStore from 'redux-mock-store';
import thunk from 'redux-thunk';
import expect from 'expect'; // You can use any testing library
import fetchMock from 'fetch-mock';
import { userConstants } from './userAuthActions';
import * as actions from './userAuthActions';

import { API_HOST } from '../../constants';
// const middlewares = [thunk];
// const mockStore = configureMockStore(middlewares);

// describe('async actions', () => {
//   afterEach(() => {
//     // clear all HTTP mocks after each test
//     nock.cleanAll();
//   });

//   it('creates LOGIN_SUCCESS when login authorization gets a 200 response', () => {
//     // Simulate a successful response
//     nock('http://localhost:5000')
//       .get('/config_api/login') // Route to catch and mock
//       .reply(200, { data: 'Logged in successfully' }); // Mock reponse code and data

//       const expectedActions = [
//         { type: userConstants.LOGIN_SUCCESS }
//       ]

//     const store = mockStore({ })
//     // Dispatch action to login user
//     return store.dispatch(actions.login('12345'))
//       .then(() => { // return of async actions
//         expect(store.getActions()).toEqual(expectedActions);
//       })
//   })

// it('creates LOGIN_FAIL if user login fails', () => {
//   nock('http://localhost:5000')
//     .persist()
//     .get('/config_api/login')
//     .reply(404, { data: { error: 404 } })

//   const expectedActions = [
//     {  type: userConstants.LOGIN_FAIL }
//   ]
//   const store = mockStore({ })

//   return store.dispatch(actions.login('12345'))
//     .then(() => { // return of async actions
//       expect(store.getActions()).toEqual(expectedActions)
//     })
// })

// });

const middlewares = [thunk];
const mockStore = configureMockStore(middlewares);

describe('async actions', () => {
  afterEach(() => {
    fetchMock.restore();
  });

  it('creates FETCH_TODOS_SUCCESS when fetching todos has been done', () => {
    fetchMock.getOnce(`${API_HOST}/config_api/login`, {
      headers: { status: 200 }
    });

    const expectedActions = [
      { type: userConstants.LOGIN_SUCCESS, status: 200 }
    ];
    const store = mockStore({});

    return store.dispatch(actions.login()).then(() => {
      // return of async actions
      expect(store.getActions()).toEqual(expectedActions);
    });
  });
});
