import * as actions from './index';
import * as types from './constants';

describe('actions', () => {
  it('storeToken should create an action to store access token value', () => {
    const token = '1234';
    const expectedAction = {
      type: types.GOOGLE_LOGIN_RESPONSE,
      token
    };
    expect(actions.storeToken(token)).toEqual(expectedAction);
  });
});
