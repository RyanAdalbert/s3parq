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
`;

export default class Header extends PureComponent {
  render() {
    const { logOutHandler } = this.props;
    return (
      <HeaderSec>
        <ul>
          <li>Welcome, Alec</li>
          <li onClick={logOutHandler}>Log out</li>
        </ul>
      </HeaderSec>
    );
  }
}
