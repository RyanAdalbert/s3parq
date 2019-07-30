import React, { PureComponent, Fragment } from 'react';

import multiFilter from '../../utils/multiFilter/multiFilter';
import PipelineModal from '../PipelineModal/PipelineModal';
import {
  modalOpen,
  modalClose
} from '../../redux/actions/pipelineActions/pipelineActions';

//Pipeline row component
export default class PipelineRow extends PureComponent {
  render() {
    const { pipelines, setFilters, dispatch, modalProps } = this.props;

    const filtered = multiFilter(pipelines, setFilters);

    const handleClick = (modalStatus, pipeline) => {
      dispatch(modalOpen(modalStatus, pipeline));
    };

    const closeModal = () => {
      dispatch(modalClose(false, {}));
    };

    const pipelineRow = filtered.map(pipeline => {
      return (
        // creates modals
        <Fragment key={pipeline.run_id.toString()}>
          <tr onClick={() => handleClick(true, pipeline)}>
            <td>{pipeline.run_id}</td>
            <td>{pipeline.name}</td>
            <td>{pipeline.brand}</td>
            <td>{pipeline.pharma_company}</td>
            <td>{pipeline.status}</td>
            <td>{pipeline.run_freq}</td>

            {/* Need to add a conditional statement here to keep from rendering all the time */}
            {/* However, we run into an issue with getting access to the component itself after we do that */}
          </tr>
          <PipelineModal
            show={this.props.modalShow}
            onHide={closeModal}
            pipelineInfo={modalProps}
          />
        </Fragment>
      );
    });

    return pipelineRow;
  }
}
