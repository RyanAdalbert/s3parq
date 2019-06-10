import React, { PureComponent } from 'react';

import multiFilter from '../../utils/multiFilter/multiFilter';
import guiModal from '../guiModal/guiModal';
import { modalToggle } from '../../redux/actions/pipelineActions/pipelineActions';
//Pipeline row component
export default class PipelineRow extends PureComponent {
  render() {
    const { pipelines, setFilters, dispatch } = this.props;

    const filtered = multiFilter(pipelines, setFilters);

    let modalClose = () => this.setState({ modalShow: false });

    const key = Object.keys(pipelines);

    const handleClick = modalState => {
      dispatch(modalToggle(modalState));
    };

    const pipelineRow = filtered.map(pipeline => {
      return (
        // creates modals
        <>
          <tr key={key + pipeline.name} onClick={() => handleClick(true)}>
            <td>{key}</td>
            <td>{pipeline.name}</td>
            <td>{pipeline.brand}</td>
            <td>{pipeline.pharma_company}</td>
            <td>{pipeline.status}</td>
            <td>{pipeline.run_freq}</td>
          </tr>

          <guiModal show={this.props.modalShow} onHide={modalClose} />
        </>
      );
    });

    return pipelineRow;
  }
}
