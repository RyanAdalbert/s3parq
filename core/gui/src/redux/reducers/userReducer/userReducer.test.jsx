import reducer from './userReducer';
import { userConstants } from '../../actions/userAuthActions/userAuthActions';

const userInfo = {
  isLoggedIn: true,
  oAuthToken: '99999',
  userName: 'Nova'
};

describe('User Auth Reducer', () => {
  it('should return the initial state', () => {
    expect(reducer(undefined, {})).toEqual({
      oAuthToken: 'loading',
      userName: 'loading',
      isLoggedIn: 'loading'
    });
  });

  it('should handle LOGIN_ATTEMPT', () => {
    expect(
      reducer(undefined, {
        type: userConstants.LOGIN_ATTEMPT
      })
    ).toEqual({
      isLoggingIn: true,
      isLoggedIn: false,
      oAuthToken: 'loading',
      userName: 'loading'
    });
  });

  it('should handle LOGIN_SUCCESS', () => {
    expect(
      reducer(undefined, {
        type: userConstants.LOGIN_SUCCESS
      })
    ).toEqual({
      error: null,
      isLoggingIn: false,
      isLoggedIn: true,
      oAuthToken: 'loading',
      userName: 'loading'
    });
  });

  it('should handle STORE_TOKEN', () => {
    const updateAction = {
      type: userConstants.STORE_TOKEN,
      payload: {
        oAuthToken: userInfo.oAuthToken,
        userName: userInfo.userName
      }
    };
    expect(reducer(undefined, updateAction)).toEqual(userInfo);
  });
});
