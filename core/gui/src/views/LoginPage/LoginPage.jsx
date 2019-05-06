import React from 'react';
import { GoogleLogin } from 'react-google-login';
import styled from 'styled-components';
import { connect } from 'react-redux';

import { login, storeToken } from '../../redux/actions/userAuthActions';

import coreLogo from '../../assets/coreLogo.png';
import Logo from '../../assets/integrichain-logo.svg';

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

    .core-powered {
      display: flex;
      align-items: center;
      margin-top: 20px;

      h5 {
        color: #4a4a4a;
        margin: 10px 0;
      }

      img {
        width: 25px;
        margin: 10px;
      }
    }
  }
`;

class LoginPage extends React.Component {
  componentDidMount() {
    localStorage.clear();
  }

  render() {
    const { dispatch } = this.props;

    // Get Response from Google and store it in state
    const responseGoogle = response => {
      const { accessToken } = response;
      const { givenName } = response.profileObj;
      console.log(response);
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
          <div className="core-powered">
            <h5 className="text">Powered by Core</h5>
            <img src={coreLogo} alt="Core Logo" />
          </div>
        </div>
      </LoginWrapper>
    );
  }
}

const mapStateToProps = state => {
  return {
    oAuthToken: state.userReducer.oAuthToken
  };
};

export default connect(mapStateToProps)(LoginPage);
