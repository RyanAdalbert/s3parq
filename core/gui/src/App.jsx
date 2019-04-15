import React from 'react';

import styled from 'styled-components';

import Sidebar from './Components/Sidebar/Sidebar';
import Header from './Components/Header/Header';

// Styles
const Wrapper = styled.div`
  display: flex;
  align-items: flex-start;
  background: #e0e0e0;
`;

const Main = styled.div`
  flex: 5;
`;

const Reactv = require('react');

console.log(Reactv.version);

const App = () => (
  <Wrapper>
    <Sidebar />
    <Main>
      <Header />
    </Main>
  </Wrapper>
);

export default App;
