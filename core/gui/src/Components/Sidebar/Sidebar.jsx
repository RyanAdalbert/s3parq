import React from 'react';
import { Link } from 'react-router-dom';
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

  .logo-container {
    display: flex;
    align-items: center;
    height: 63px;
    border-bottom: 1px solid #f3f3f3;
  }

  img {
    width: 100%;
  }

  ul {
    padding: 0;
    text-align: left;
    list-style: none;
    font-size: 1rem;

    li {
      padding: 5px;
      &:hover {
        background-color: #f3f3f3;
      }
    }

    a {
      color: #000;

      &:hover {
        text-decoration: none;
      }
    }
  }
`;

const Sidebar = () => (
  <SidebarWrapper>
    <div className="logo-container">
      <img src={logo} alt="Integrichain Logo" />
    </div>
    <ul>
      <li>
        <Link to="/admin/pipelineindex">Pipeline Index</Link>
      </li>
      <li>
        <Link to="/admin/createpipeline">Create Pipeline</Link>
      </li>
    </ul>
  </SidebarWrapper>
);

export default Sidebar;
