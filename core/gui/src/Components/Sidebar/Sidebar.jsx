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
  grid-area: sb;

  img {
    width: 100%;
    max-width: 200px;
    margin: 0 auto;
    padding-bottom: 5px;
    border-bottom: 1px solid #ccc;
  }

  ul {
    margin: 20px 0;
    padding: 0;
    list-style: none;
    font-size: 1.5rem;
  }
`;

const Sidebar = () => (
  <SidebarWrapper>
    <img src={logo} alt="Integrichain Logo" />
    <ul>
      <li>Pipelines</li>
    </ul>
  </SidebarWrapper>
);

export default Sidebar;
