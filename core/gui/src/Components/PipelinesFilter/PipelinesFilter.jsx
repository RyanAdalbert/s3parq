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

    const dropdownBrands =
      brands !== undefined
        ? brands.map(brand => {
            return (
              <Dropdown.Item as="button" key={brand} eventKey={brand}>
                {brand}
              </Dropdown.Item>
            );
          })
        : null;

    const dropdownCompanies =
      companies !== undefined
        ? companies.map(company => {
            return (
              <Dropdown.Item as="button" key={company} eventKey={company}>
                {company}
              </Dropdown.Item>
            );
          })
        : null;

    const dropdownTypes =
      types !== undefined
        ? types.map(type => {
            return (
              <Dropdown.Item as="button" key={type} eventKey={type}>
                {type}
              </Dropdown.Item>
            );
          })
        : null;

    const dropdownStatus =
      status !== undefined
        ? status.map(stat => {
            return (
              <Dropdown.Item as="button" key={stat} eventKey={stat}>
                {stat}
              </Dropdown.Item>
            );
          })
        : null;

    return (
      <PipelineFilterContainer>
        <Dropdown className="dropdown-container" size="sm">
          <DropdownButton
            title="Brand"
            onSelect={function(evt) {
              console.log(evt);
            }}
          >
            {dropdownBrands}
          </DropdownButton>
          <DropdownButton
            title="Companies"
            onSelect={function(evt) {
              console.log(evt);
            }}
          >
            {dropdownCompanies}
          </DropdownButton>
          <DropdownButton
            title="Types"
            onSelect={function(evt) {
              console.log(evt);
            }}
          >
            {dropdownTypes}
          </DropdownButton>
          <DropdownButton
            title="Status"
            onSelect={function(evt) {
              console.log(evt);
            }}
          >
            {dropdownStatus}
          </DropdownButton>
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
