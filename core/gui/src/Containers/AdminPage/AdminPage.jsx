import React from 'react';

import styled from 'styled-components';

import Sidebar from '../../components/Sidebar/Sidebar';
import Header from '../../components/Header/Header';
import Footer from '../../components/Footer/Footer';
import Dashboard from '../../views/Dashboard/Dashboard';

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
