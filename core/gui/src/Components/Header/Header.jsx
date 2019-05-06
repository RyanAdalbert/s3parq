import React, { PureComponent } from 'react';

import styled from 'styled-components';

// Styles
const HeaderSec = styled.section`
  display: flex;
  justify-content: flex-end;
  padding: 6px 5%;
  background: #004cae;
  color: #fff;

  p {
    color: #fff;
  }

  .user-info {
    h3 {
      margin-bottom: 5px;
    }
    p {
      margin-top: 5px;
      cursor: pointer;
    }
  }
`;

export default class Header extends PureComponent {
  render() {
    const { logOutHandler, userName } = this.props;
    return (
      <HeaderSec>
        <div className="user-info">
          <h3>Welcome, {userName}</h3>
          <p onClick={logOutHandler}>Log out</p>
        </div>
      </HeaderSec>
    );
  }
}
