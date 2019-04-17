import React from 'react';
import { GoogleLogin } from 'react-google-login';
import styled from 'styled-components';

import Logo from '../../Assets/integrichain-logo.svg';

// Styles
const LoginWrapper = styled.div`
  display: flex;
  height: 99vh;
  width: 100%;
  margin: auto;
  background-color: #fff;

  .LoginContainer {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: auto;
    padding: 30px 50px;
    border: 1px solid #e4e4e4;
    border-radius: 4px;
    background-color: #f7f7f7;
    box-shadow: 0px 3px 3px 0px #999999;

    .ButtonWrapper {
      margin: 10px 0 0 0;
      border: none;
    }
  }
`;

const responseGoogle = response => {
  console.log(response.accessToken);
  return response.accessToken;
};

const Login = () => (
  <LoginWrapper>
    <div className="LoginContainer">
      <img src={Logo} alt="Integrichain Logo" />
      <p>Data Transform Admin Panel</p>
      <div className="ButtonWrapper">
        <GoogleLogin
          clientId="437067415795-3hb6psqn86pu7ri76k594do568buebam.apps.googleusercontent.com"
          buttonText="Login"
          onSuccess={responseGoogle}
          onFailure={responseGoogle}
        />
      </div>
    </div>
  </LoginWrapper>
);

export default Login;
