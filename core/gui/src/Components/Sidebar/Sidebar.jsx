import React from 'react';

import styled from 'styled-components';

import logo from '../../assets/integrichain-logo.svg';

// Styles
const SidebarWrapper = styled.div`
  display: flex;
  flex: 1;
  flex-direction: column;
  height: 99vh;
  padding: 10px 10px 0 10px;
  background-color: #fff;

  img {
    width: 100%;
    max-width: 200px;
    margin: 0 auto;
    padding-bottom: 5px;
    border-bottom: 1px solid #ccc;
  }
`;

const Sidebar = () => (
  <SidebarWrapper>
    <img src={logo} alt="Integrichain Logo" />
  </SidebarWrapper>
);

export default Sidebar;
