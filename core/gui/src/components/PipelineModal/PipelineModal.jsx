import React from 'react';
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';

class PipelineModal extends React.Component {
  render() {
    const {
      brand,
      name,
      description,
      type,
      states,
      transformations
    } = this.props.pipelineInfo;

    if (this.props.show === false) {
      return null;
    }

    return (
      <Modal
        {...this.props}
        size="lg"
        aria-labelledby="contained-modal-title-vcenter"
        centered
      >
        <Modal.Header closeButton>
          <Modal.Title id="contained-modal-title-vcenter">
            {brand} : {name}
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <h3>Description:</h3>
          <p>{description}</p>
          <h4>Type:</h4>
          <p>{type}</p>
          <h4>States:</h4>
          <div>
            <ul>
              {states.map((stateInfo, index) => (
                <li key={index}>{stateInfo}</li>
              ))}
            </ul>
          </div>
          <h4>Transforms:</h4>
          <div>
            <ul>
              {transformations.map((transform, index) => (
                <li key={index}>{transform}</li>
              ))}
            </ul>
          </div>
        </Modal.Body>
        <Modal.Footer>
          <Button onClick={this.props.onHide}>Close</Button>
        </Modal.Footer>
      </Modal>
    );
  }
}

export default PipelineModal;
