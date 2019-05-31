import React from 'react';
import PropTypes from 'prop-types';
import Dropdown from 'react-bootstrap/Dropdown';
import DropdownButton from 'react-bootstrap/DropdownButton';
import styled from 'styled-components';

import {
  setFilterBrand,
  setFilterCompany,
  setFilterType,
  setFilterStatus
} from '../../redux/actions/filterActions/filterActions';

class DropdownButtons extends React.Component {
  render() {
    const { brands, companies, types, status } = this.props.filters;

    //Check to make sure Attributes (Brands, Companies, Types, Status) are being hydrated in the Store if so render dropdown buttons
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

    // Dispatch corresponding button action that sets the filter in the store with the correct selection
    const handleSelect = (evt, buttonName) => {
      const { dispatch } = this.props;
      if (buttonName === 'brand') {
        dispatch(setFilterBrand(evt));
      }
      if (buttonName === 'company') {
        dispatch(setFilterCompany(evt));
      }
      if (buttonName === 'type') {
        dispatch(setFilterType(evt));
      }
      if (buttonName === 'status') {
        dispatch(setFilterStatus(evt));
      }
    };

    return (
      <>
        <DropdownButton
          title="Brand"
          onSelect={evt => handleSelect(evt, 'brand')}
        >
          {dropdownBrands}
        </DropdownButton>
        <DropdownButton
          title="Companies"
          onSelect={evt => handleSelect(evt, 'company')}
        >
          {dropdownCompanies}
        </DropdownButton>
        <DropdownButton
          title="Types"
          onSelect={evt => handleSelect(evt, 'type')}
        >
          {dropdownTypes}
        </DropdownButton>
        <DropdownButton
          title="Status"
          onSelect={evt => handleSelect(evt, 'status')}
        >
          {dropdownStatus}
        </DropdownButton>
      </>
    );
  }
}

DropdownButtons.propTypes = {};

export default DropdownButtons;
