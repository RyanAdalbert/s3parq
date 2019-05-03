// import * as actions from './userActions';
// import { userConstants } from './userActions';
// import fetchMock from 'fetch-mock';
// import configureMockStore from 'redux-mock-store';

// //sync action tests
// describe('actions', () => {
//   //Test Google Response Action Creator
//   it('googleResponseSuccess() should create an action to store access token, refresh token and userName values', () => {
//     const oAuthToken = '1234';
//     const refreshToken = '5678';
//     const userName = 'Nova';

//     const expectedAction = {
//       type: userConstants.GOOGLE_RESPONSE_SUCCESS,
//       payload: {
//         oAuthToken,
//         refreshToken,
//         userName
//       }
//     };
//     expect(
//       actions.googleResponseSuccess(oAuthToken, refreshToken, userName)
//     ).toEqual(expectedAction);
//   });
// });

// //variables for async actions tests
// const middlewares = [thunk];
// const mockStore = configureMockStore(middlewares);

// //async action tests
// describe('async actions', () => {
//   afterEach(() => {
//     fetchMock.restore()
//   })
//     //Test Login Async Action Creator
//     it('login() should log the user in after getting success response from API', () => {

//       const oAuthToken = '1234';

//       const expectedActions = [
//         { type: userConstants.LOGIN_REQUEST },
//         { type: userConstants.LOGIN_SUCCESS, body: { response: '200' } }
//       ];

//       const store = mockStore( {  } )
//     });
// })
