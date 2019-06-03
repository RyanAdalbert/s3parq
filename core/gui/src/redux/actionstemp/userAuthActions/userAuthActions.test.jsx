import * as actions from './userAuthActions';
import { userConstants } from './userAuthActions';

describe('Authentication Actions', () => {
  it('should create an action to store token, and user name', () => {
    const token = '1234';
    const user = 'The Night King';
    const expectedAction = {
      type: userConstants.STORE_TOKEN,
      token,
      user
    };
    expectedAction(actions.storeToken(token, user).toEqual.expectedAction);
  });
});
