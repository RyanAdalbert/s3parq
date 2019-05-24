import React from 'react';
import PropTypes from 'prop-types';
import Dropdown from 'react-bootstrap/Dropdown';
import DropdownButton from 'react-bootstrap/DropdownButton';

class PipelinesFilter extends React.Component {
  render() {
    return (
      <Dropdown>
        <DropdownButton title="Brand" />
      </Dropdown>
    );
  }
}

export default PipelinesFilter;

PipelinesFilter.propTypes = {
  pipeline: PropTypes.shape({
    brand: PropTypes.string.isRequired
  })
};
