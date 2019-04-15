import React from 'react';

import styled from 'styled-components';

import logo from '../../Assets/integrichain-logo.svg';

const SidebarWrapper = styled.div`
  display: flex;
  flex-direction: column;
  background-color: #fff;
  padding: 10px;
  height: 100vh;
`;

const Sidebar = () => (
  <SidebarWrapper>
    <img src={logo} alt="Integrichain Logo" />
  </SidebarWrapper>
);

export default Sidebar;
