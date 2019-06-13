import React, { PureComponent } from 'react';

import multiFilter from '../../utils/multiFilter/multiFilter';
import PipelineModal from '../PipelineModal/PipelineModal';
import {
  modalOpen,
  modalClose
} from '../../redux/actions/pipelineActions/pipelineActions';
//Pipeline row component
export default class PipelineRow extends PureComponent {
  render() {
    const { pipelines, setFilters, dispatch } = this.props;

    const filtered = multiFilter(pipelines, setFilters);

    const key = Object.keys(pipelines);

    const handleClick = (modalStatus, pipeline) => {
      dispatch(modalOpen(modalStatus, pipeline));
    };

    const closeModal = () => {
      dispatch(modalClose(false));
    };

    const pipelineRow = filtered.map(pipeline => {
      return (
        // creates modals
        <>
          <tr
            key={key + pipeline.name}
            onClick={() => handleClick(true, pipeline)}
          >
            <td>{key}</td>
            <td>{pipeline.name}</td>
            <td>{pipeline.brand}</td>
            <td>{pipeline.pharma_company}</td>
            <td>{pipeline.status}</td>
            <td>{pipeline.run_freq}</td>
            {/*console.log(pipeline)*/}
          </tr>

          <PipelineModal show={this.props.modalShow} onHide={closeModal} />
        </>
      );
    });

    return pipelineRow;
  }
}
