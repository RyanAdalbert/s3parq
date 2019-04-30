import * as actions from './userActions';
import { userConstants } from './userActions';

describe('user actions', () => {
  //Test Google Response Action Creator
  it('googleResponseSuccess should create an action to store access token, refresh token and userName values', () => {
    const oAuthToken = '1234';
    const refreshToken = '5678';
    const userName = 'Nova';

    const expectedAction = {
      type: userConstants.GOOGLE_RESPONSE_SUCCESS,
      payload: {
        oAuthToken,
        refreshToken,
        userName
      }
    };
    expect(
      actions.googleResponseSuccess(oAuthToken, refreshToken, userName)
    ).toEqual(expectedAction);
  });

  //Test Login Async Action Creator
  it('login should create and action to POST the access token to the Flask API', () => {
    const oAuthToken = '1234';

    const expectedAction = {
      type: LOGIN_REQUEST
    };
  });
});
