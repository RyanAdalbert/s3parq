import React from 'React';
import { shallow } from 'enzyme';
import userAuth from './userAuth';

import mockGoogleObj from '../../../__mocks__/mockGoogleObj';

describe('userAuth', () => {
  const results = userAuth(mockGoogleObj);

  it('Gets access Token from Google User Object', () => {
    results.expect(types.LOGIN_USER).toBe('12345');
  });

  it('Stores Access Token in Redux', () => {});

  it('POSTs Access Token to Flask API', {});

  it('Sends Returns Response From Flask', () => {});
});
