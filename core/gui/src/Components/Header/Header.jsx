import React from 'react';

import styled from 'styled-components';

const Wrapper = styled.div`
  display: flex;
  padding: 0 5%;
  justify-content: flex-end;
  width: 100%;
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
