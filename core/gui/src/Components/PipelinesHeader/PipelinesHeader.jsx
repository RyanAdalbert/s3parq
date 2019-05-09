import React, { PureComponent } from 'react';

import styled from 'styled-components';

// Styles
const HeaderSec = styled.section`
  display: flex;
  justify-content: flex-start;
  width: 100%;
  padding: 10px;
  background: #fff;
  color: #fff;

  p {
    margin: 0;
  }
`;

export default class PipelineHeader extends PureComponent {
  render() {
    return (
      <HeaderSec>
        <p>Pipeline Dashboard Header</p>
      </HeaderSec>
    );
  }
}
