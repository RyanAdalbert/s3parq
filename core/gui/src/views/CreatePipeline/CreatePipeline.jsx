import React from 'react';
import styled from 'styled-components';

// Styles
const DashboardContainer = styled.section`
  display: flex;
  flex: 1;
  flex-direction: column;
  margin: 50px;
`;

class CreatePipeline extends React.Component {
  render() {
    return (
      <DashboardContainer>
        <div>Create Pipeline</div>
      </DashboardContainer>
    );
  }
}

export default CreatePipeline;
