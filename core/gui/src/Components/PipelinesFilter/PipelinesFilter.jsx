import React from 'react';
import PropTypes from 'prop-types';
import Dropdown from 'react-bootstrap/Dropdown';
import DropdownButton from 'react-bootstrap/DropdownButton';

class PipelinesFilter extends React.Component {
  render() {
    const { pipelines } = this.props;

    const dropdownItemsArr = [];
    const dropdownItems = pipelines.map(pipeline => {
      const key = Object.keys(pipeline);
      return <Dropdown.Item as="button">{pipeline[key].brand}</Dropdown.Item>;
    });

    return (
      <Dropdown>
        <DropdownButton title="Brand">{dropdownItems}</DropdownButton>
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
