import React from 'react';
import PropTypes from 'prop-types';
import Dropdown from 'react-bootstrap/Dropdown';
import DropdownButton from 'react-bootstrap/DropdownButton';
import styled from 'styled-components';

import { setFilter } from '../../redux/actions/filterActions/filterActions';

class DropdownButtons extends React.Component {
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

    const handleSelect = evt => {
      const { dispatch } = this.props;
      dispatch(setFilter(evt));
    };

    return (
      <>
        <DropdownButton title="Brand" onSelect={evt => handleSelect(evt)}>
          {dropdownBrands}
        </DropdownButton>
        <DropdownButton title="Companies" onSelect={evt => handleSelect(evt)}>
          {dropdownCompanies}
        </DropdownButton>
        <DropdownButton title="Types" onSelect={evt => handleSelect(evt)}>
          {dropdownTypes}
        </DropdownButton>
        <DropdownButton title="Status" onSelect={evt => handleSelect(evt)}>
          {dropdownStatus}
        </DropdownButton>
      </>
    );
  }
}

export default DropdownButtons;
