import * as actions from './index';
import * as types from './constants';

describe('actions', () => {
  it('storeToken should create an action to store access token value', () => {
    const token = '1234';
    const expectedAction = {
      type: types.STORE_TOKEN,
      token
    };
    expect(actions.storeToken(token)).toEqual(expectedAction);
  });

  it('storeName should create an action to store given name value', () => {
    const name = 'Nova';
    const expectedAction = {
      type: types.STORE_NAME,
      name
    };
    expect(actions.storeName(name)).toEqual(expectedAction);
  });
});
