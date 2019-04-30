import React from 'react';

import styled from 'styled-components';

import Sidebar from '../../Components/Sidebar/Sidebar';
import Header from '../../Components/Header/Header';
import Footer from '../../Components/Footer/Footer';
import Dashboard from '../../Views/Dashboard/Dashboard';

// Styles
const AdminWrapper = styled.div`
  display: flex;
  align-items: flex-start;
  background: #e0e0e0;
`;

const Main = styled.div`
  flex: 5;
`;

const AdminPage = () => (
  <AdminWrapper>
    <Sidebar />
    <Main>
      <Header />
      <Dashboard />
      <Footer />
    </Main>
  </AdminWrapper>
);

export default AdminPage;
