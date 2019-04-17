import React from 'react';

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

const User = 'Alec';

const Header = () => (
  <HeaderSec>
    <p>
      Welcome,
      {`${User}`}
    </p>
  </HeaderSec>
);

export default Header;
