import React from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';

const PipelineList = styled.ul`
  margin: 0;
  padding: 0;
`;

const PipelineRow = styled.li`
  display: grid;
  list-style: none;
  grid-template-columns: 3fr 2fr 3fr 1fr 1fr;
  grid-column-gap: 5px;
  border-left: 1px solid #adadad;
  border-right: 1px solid #adadad;

  &:nth-child(odd) {
    background-color: #ccc;
  }

  &:last-child {
    border-bottom: 1px solid #ccc;
  }

  div {
    padding: 10px 0 10px 10px;
    border-right: 1px solid #adadad;

    &:last-child {
      border-right: none;
    }
  }
`;

class Pipelines extends React.Component {
  render() {
    const { pipelines } = this.props;

    const pipeline = pipelines.map(pipeline => {
      const key = Object.keys(pipeline);

      return (
        <PipelineRow key={key}>
          <div>{pipeline[key].name}</div>
          <div>{pipeline[key].brand}</div>
          <div>{pipeline[key].pharma_company}</div>
          <div>{pipeline[key].status}</div>
          <div>{pipeline[key].run_freq}</div>
        </PipelineRow>
      );
    });

    return (
      <div>
        <PipelineList>{pipeline}</PipelineList>
      </div>
    );
  }
}

export default Pipelines;

Pipelines.propTypes = {
  pipeline: PropTypes.shape({
    name: PropTypes.string.isRequired,
    brand: PropTypes.string.isRequired,
    pharma_company: PropTypes.string.isRequired,
    type: PropTypes.string.isRequired,
    status: PropTypes.string.isRequired,
    description: PropTypes.string.isRequired,
    run_freq: PropTypes.string.isRequired,
    states: PropTypes.object.isRequired,
    transformations: PropTypes.array.isRequired
  })
};
