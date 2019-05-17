import React from 'react';
import PropTypes from 'prop-types';
import Table from 'react-bootstrap/Table';
import styled from 'styled-components';

import PipelineRow from '../PipelineRow/PipelineRow';

const TableContainer = styled.div`
  h3 {
    margin-bottom: 10px;
    padding: 5px;
    border-bottom: 1px solid #ccc;
  }

  thead {
    background-color: #fff;
    padding: 5px;

    h5 {
      margin: 5px 0;
    }
  }

  tbody {
    border: 1px solid #000;
  }
`;

class Pipelines extends React.Component {
  render() {
    return (
      <TableContainer>
        <h3>Pipeline Index</h3>
        <Table striped bordered hover responsive size="sm">
          <thead>
            <tr>
              <th>
                <h5>#</h5>
              </th>
              <th>
                <h5>Name</h5>
              </th>
              <th>
                <h5>Brand</h5>
              </th>
              <th>
                <h5>Pharma Company</h5>
              </th>
              <th>
                <h5>Status</h5>
              </th>
              <th>
                <h5>Run Freq</h5>
              </th>
            </tr>
          </thead>
          <tbody>
            <PipelineRow {...this.props} />
          </tbody>
        </Table>
      </TableContainer>
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
