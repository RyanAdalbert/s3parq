import React from 'react';
import { GoogleLogin } from 'react-google-login';
import styled from 'styled-components';
import { connect } from 'react-redux';
import Logo from '../../assets/integrichain-logo.svg';

import { login, storeToken } from '../../redux/actions/userAuthActions';

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
    background-color: #efefef;
    box-shadow: 0px 3px 3px 0px #999999;

    .ButtonWrapper {
      margin: 10px 0 0 0;
      border: none;
    }

    .login-subtext {
      font-size: 10px;
    }
  }
`;

class LoginPage extends React.Component {
  render() {
    const { dispatch } = this.props;

    // Get Response from Google and store it in state
    const responseGoogle = response => {
      const { accessToken } = response;
      const { givenName } = response.profileObj;

      dispatch(storeToken(accessToken, givenName));
      dispatch(login(accessToken));
    };

    return (
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
          <p className="login-subtext">Powered by core</p>
        </div>
      </LoginWrapper>
    );
  }
}

const mapStateToProps = state => {
  return {
    oAuthToken: state.oAuthToken
  };
};

export default connect(mapStateToProps)(LoginPage);
