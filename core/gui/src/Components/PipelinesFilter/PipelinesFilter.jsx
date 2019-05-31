import React from 'react';
import PropTypes from 'prop-types';
import Dropdown from 'react-bootstrap/Dropdown';
import styled from 'styled-components';

import DropdownButtons from '../DropdownButtons/DropdownButtons';

const PipelineFilterContainer = styled.div`
  margin-bottom: 10px;

  .dropdown-container {
    width: 100%;
    display: flex;
    justify-content: flex-start;
  }

  .dropdown {
    margin-right: 5px;
  }
`;

class PipelinesFilter extends React.Component {
  render() {
    return (
      <PipelineFilterContainer>
        <Dropdown className="dropdown-container" size="sm">
          <DropdownButtons {...this.props} />
        </Dropdown>
      </PipelineFilterContainer>
    );
  }
}

export default PipelinesFilter;

PipelinesFilter.propTypes = {
  pipeline: PropTypes.shape({
    brand: PropTypes.string.isRequired
  })
};
