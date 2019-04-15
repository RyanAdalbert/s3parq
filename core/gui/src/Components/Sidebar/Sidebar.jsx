import React from 'react';

import styled from 'styled-components';

import logo from '../../Assets/integrichain-logo.svg';

// Styles
const SidebarWrapper = styled.div`
  display: flex;
  flex: 1;
  flex-direction: column;
  background-color: #fff;
  padding: 10px 10px 0 10px;
  height: 99vh;

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
