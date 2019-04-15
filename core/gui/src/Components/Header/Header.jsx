import React from 'react';

import styled from 'styled-components';

// Styles
const Wrapper = styled.div`
  display: flex;
  padding: 6px 5%;
  justify-content: flex-end;
  background: #004cae;
  color: #fff;
`;

const User = 'Alec';

const Header = () => (
  <Wrapper>
    <p>
      Welcome,
      {` ${User}`}
    </p>
  </Wrapper>
);

export default Header;
