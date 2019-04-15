import React from 'react';
import styled from 'styled-components';

import Routes from './Routes/Routes';
import Sidebar from './Components/Sidebar/Sidebar';
import Header from './Components/Header/Header';

// Styles
const Wrapper = styled.div`
  display: flex;
  align-items: flex-start;
  background: #e0e0e0;
`;

const App = () => (
  <Wrapper>
    <Sidebar />
    <Header />
  </Wrapper>
);

export default App;
