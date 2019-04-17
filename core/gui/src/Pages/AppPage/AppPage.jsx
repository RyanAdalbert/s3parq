import React from 'react';

import styled from 'styled-components';

import Sidebar from '../../Components/Sidebar/Sidebar';
import Header from '../../Components/Header/Header';
import Footer from '../../Components/Footer/Footer';

// Styles
const AppWrapper = styled.div`
  display: flex;
  align-items: flex-start;
  background: #e0e0e0;
`;

const Main = styled.div`
  flex: 5;
`;

const AppPage = () => (
  <AppWrapper>
    <Sidebar />
    <Main>
      <Header />

      <Footer />
    </Main>
  </AppWrapper>
);

export default AppPage;
