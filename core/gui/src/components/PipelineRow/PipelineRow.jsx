import React, { PureComponent } from 'react';
// import Button from 'react-bootstrap/Button';
// import Modal from 'react-bootstrap/Modal';
import multiFilter from '../../utils/multiFilter/multiFilter';

//Pipeline row component
export default class PipelineRow extends PureComponent {
  render() {
    const { pipelines } = this.props;
    const { setFilters } = this.props;

    const filtered = multiFilter(pipelines, setFilters);

    const key = Object.keys(pipelines);
    const pipelineRow = filtered.map(pipeline => {
      return (
        // creates modals
        <tr key={key + pipeline.name}>
          <td>{key}</td>
          <td>{pipeline.name}</td>
          <td>{pipeline.brand}</td>
          <td>{pipeline.pharma_company}</td>
          <td>{pipeline.status}</td>
          <td>{pipeline.run_freq}</td>
        </tr>
      );
    });

    return pipelineRow;
  }
}
