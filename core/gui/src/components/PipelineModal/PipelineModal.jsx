import React from 'react';
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';

class PipelineModal extends React.Component {
  render() {
    console.log(this.props);
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
            {this.props.pipelineInfo.brand} : {this.props.pipelineInfo.name}
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <h4>Description</h4>
          <p>{this.props.pipelineInfo.description}</p>
          <h3>Type</h3>
          <p>{this.props.pipelineInfo.type}</p>
          <h3>States</h3>
          <div>
            <ul>
              {this.props.pipelineInfo.states.map((stateInfo, index) => (
                <li key={index}>{stateInfo}</li>
              ))}
            </ul>
          </div>
          <h3>Transforms</h3>
          <div>
            <ul>
              {this.props.pipelineInfo.transformations.map(
                (transform, index) => (
                  <li key={index}>{transform}</li>
                )
              )}
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
