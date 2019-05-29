import React from 'react';
import PropTypes from 'prop-types';
import Dropdown from 'react-bootstrap/Dropdown';
import DropdownButton from 'react-bootstrap/DropdownButton';
import styled from 'styled-components';

const PipelineFilterContainer = styled.div`
  margin-bottom: 10px;

  .dropdown-container {
    width: 100%;
    display: flex;
    justify-content: flex-start;

    .dropdown {
      margin-right: 5px;

      button {
        padding: 2px 10px;
      }
    }
  }
`;

class PipelinesFilter extends React.Component {
  render() {
    const { brands, companies, types, status } = this.props.filters;

    const dropdownBrands = brands.map(brand => {
      return (
        <Dropdown.Item as="button" key={brand}>
          {brand}
        </Dropdown.Item>
      );
    });

    const dropdownCompanies = companies.map(company => {
      return (
        <Dropdown.Item as="button" key={company}>
          {company}
        </Dropdown.Item>
      );
    });

    const dropdownTypes = types.map(type => {
      return (
        <Dropdown.Item as="button" key={type}>
          {type}
        </Dropdown.Item>
      );
    });

    const dropdownStatus = status.map(stat => {
      return (
        <Dropdown.Item as="button" key={stat}>
          {stat}
        </Dropdown.Item>
      );
    });

    return (
      <PipelineFilterContainer>
        <Dropdown className="dropdown-container" size="sm">
          <DropdownButton title="Brand">{dropdownBrands}</DropdownButton>
          <DropdownButton title="Companies">{dropdownCompanies}</DropdownButton>
          <DropdownButton title="Types">{dropdownTypes}</DropdownButton>
          <DropdownButton title="Status">{dropdownStatus}</DropdownButton>
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
