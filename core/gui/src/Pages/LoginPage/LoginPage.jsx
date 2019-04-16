import React from 'react';

import styled from 'styled-components';

import Login from '../../Components/Login/Login';

// Styles
const LoginWrapper = styled.div`
  display: flex;
`;

const LoginPage = () => (
  <LoginWrapper>
    <Login />
  </LoginWrapper>
);

export default LoginPage;
