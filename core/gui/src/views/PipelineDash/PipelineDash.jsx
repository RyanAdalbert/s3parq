import React from 'react';
import styled from 'styled-components';

import PipelineData from '../../containers/PipelineData/PipelineData';
import Pipelines from '../../components/Pipelines/Pipelines';

// Styles
const DashboardContainer = styled.div`
  display: flex;
  margin: 50px;

  p {
    color: #000;
  }
`;

//Wrap our Pipelines component in and HOC to pass the data
const PipelinesWithData = PipelineData(Pipelines);

class PipelineDash extends React.Component {
  render() {
    return (
      <DashboardContainer>
        <PipelinesWithData />
      </DashboardContainer>
    );
  }
}

export default PipelineDash;
