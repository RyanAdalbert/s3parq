import React from 'React';
import { shallow } from 'enzyme';
import UserAuth from './UserAuth';

import mockGoogleObj from '../../../__mocks__/mockGoogleObj';

describe('UserAuth', () => {
  const results = UserAuth(mockGoogleObj);

  it('Pulls Access Token out of User Object', () => {
    results.expect(USER_TOKEN).toBe('12345');
  });

  it('Stores Access Token in Redux', () => {});

  it('POSTs Access Token to Flask API', {});

  it('Sends Returns Response From Flask', () => {});
});
