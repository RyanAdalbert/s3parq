import React from 'react';

import styled from 'styled-components';

// Styles
const DashboardContainer = styled.div`
  display: flex;

  p {
    color: #000;
  }
`;

const Dashboard = () => (
  <DashboardContainer>
    <p>Dashboard.</p>
  </DashboardContainer>
);

export default Dashboard;
