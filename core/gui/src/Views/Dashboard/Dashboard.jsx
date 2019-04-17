import React from 'react';

import styled from 'styled-components';

// Styles
const Wrapper = styled.div`
  display: flex;
  background-color: green;

  p {
    color: #000;
  }
`;

const Dashboard = () => (
  <Wrapper>
    <p>Dashboard.</p>
  </Wrapper>
);

export default Dashboard;
