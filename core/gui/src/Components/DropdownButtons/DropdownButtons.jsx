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
          title={this.props.brand}
          onSelect={evt => handleSelect(evt, 'brand')}
        >
          <Dropdown.Item as="button" key="Brand" eventKey="Brand">
            Brand
          </Dropdown.Item>
          {dropdownBrands}
        </DropdownButton>
        <DropdownButton
          title={this.props.company}
          onSelect={evt => handleSelect(evt, 'company')}
        >
          <Dropdown.Item as="button" key="Company" eventKey="Company">
            Company
          </Dropdown.Item>
          {dropdownCompanies}
        </DropdownButton>
        <DropdownButton
          title={this.props.type}
          onSelect={evt => handleSelect(evt, 'type')}
        >
          <Dropdown.Item as="button" key="Type" eventKey="Type">
            Type
          </Dropdown.Item>
          {dropdownTypes}
        </DropdownButton>
        <DropdownButton
          title={this.props.status}
          onSelect={evt => handleSelect(evt, 'status')}
        >
          <Dropdown.Item as="button" key="Status" eventKey="Status">
            Status
          </Dropdown.Item>
          {dropdownStatus}
        </DropdownButton>
      </>
    );
  }
}

DropdownButtons.propTypes = {};

export default DropdownButtons;
