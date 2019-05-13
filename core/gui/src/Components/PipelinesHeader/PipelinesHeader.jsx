import React, { PureComponent } from 'react';

import styled from 'styled-components';

// Styles
const HeaderSec = styled.div`
  ul {
    margin: 0;
    padding: 0;
    display: grid;
    list-style: none;
    grid-template-columns: 3fr 2fr 3fr 1fr 1fr;
    grid-column-gap: 5px;
    background: #fff;
    list-style: none;
    border: 1px solid #adadad;

    li {
      padding: 10px 0 10px 10px;
      border-right: 1px solid #adadad;

      &:last-child {
        border-right: none;
      }
    }
  }
`;

export default class PipelineHeader extends PureComponent {
  render() {
    return (
      <HeaderSec>
        <h2>Pipelines</h2>
        <ul>
          <li>Name</li>
          <li>Brand</li>
          <li>Pharma Company</li>
          <li>Status</li>
          <li>Run Freq.</li>
        </ul>
      </HeaderSec>
    );
  }
}
