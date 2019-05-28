import React from 'react';
import styled from 'styled-components';

import PipelineData from '../../containers/PipelineData/PipelineData';
import Pipelines from '../../components/Pipelines/Pipelines';
import PipelinesFilter from '../../components/PipelinesFilter/PipelinesFilter';

// Styles
const DashboardContainer = styled.section`
  display: flex;
  flex: 1;
  flex-direction: column;
  margin: 50px;

  .PipelinesWithData {
    width: 100%;
  }

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
        <PipelinesWithData className="PipelinesWithData" {...this.props} />
      </DashboardContainer>
    );
  }
}

export default PipelineDash;
