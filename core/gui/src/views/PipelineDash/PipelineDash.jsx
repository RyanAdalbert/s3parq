import React from 'react';
import styled from 'styled-components';

import pipelineData from '../../containers/PipelineData/PipelineData';
import PipeLines from '../../components/Pipelines/Pipelines';

// Styles
const DashboardContainer = styled.div`
  display: flex;

  p {
    color: #000;
  }
`;

//Wrap our Pipelines component in and HOC to pass the data
const PipelinesWithData = pipelineData(PipeLines);

const Dashboard = () => (
  <DashboardContainer>
    <PipelinesWithData />
  </DashboardContainer>
);

export default Dashboard;
