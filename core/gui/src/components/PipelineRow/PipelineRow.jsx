import React, { PureComponent } from 'react';
// import Button from 'react-bootstrap/Button';
// import Modal from 'react-bootstrap/Modal';

//Pipeline row component
export default class PipelineRow extends PureComponent {
  render() {
    const { pipelines } = this.props;
    const pipelineRow = pipelines.map(pipeline => {
      const key = Object.keys(pipeline);

      return (
        <tr key={key}>
          <td>{key}</td>
          <td>{pipeline[key].name}</td>
          <td>{pipeline[key].brand}</td>
          <td>{pipeline[key].pharma_company}</td>
          <td>{pipeline[key].status}</td>
          <td>{pipeline[key].run_freq}</td>
        </tr>
      );
    });

    return pipelineRow;
  }
}
