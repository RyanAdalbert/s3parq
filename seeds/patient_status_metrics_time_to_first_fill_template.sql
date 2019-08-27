BEGIN;
  INSERT INTO transformation_templates
    (name, variable_structures, pipeline_state_type_id, last_actor)
  VALUES
    ('patient_status_standardize_numbers',
      '{
          "trans_id":{"datatype": "str", "description": "Column name to use for Transaction ID"},
          "medication":{"datatype": "str", "description": "Column name to use for Medication"},
          "brand_col":{"datatype": "str", "description": "Column name to use for Brand"},
          "patient_id":{"datatype": "str", "description": "Column name to use for Patient ID"},
          "pharmacy":{"datatype": "str", "description": "Column name to use for Pharmacy"},
          "status_date":{"datatype": "str", "description": "Column name to use for Status Date"},
          "referral_date":{"datatype": "str", "description": "Column name to use for Referral Date"},
          "status":{"datatype": "str", "description": "Column name to use for Status"},
          "substatus":{"datatype": "str", "description": "Column name to use for Substatus"},
          "cust_status":{"datatype": "str", "description": "Column name to use for Customer Status"},
          "cust_status_desc":{"datatype": "str", "description": "Column name to use for Customer Status Description"},
          "payer":{"datatype": "str", "description": "Column name to use for Primary Payer"},
          "payer_type":{"datatype": "str", "description": "Column name to use for Primary Payer Type"},
          "hcp_first_name":{"datatype": "str", "description": "Column name to use for Provider First Name"},
          "hcp_last_name":{"datatype": "str", "description": "Column name to use for Provider Last Name"},
          "hcp_npi":{"datatype": "str", "description": "Column name to use for Provider NPI"},
          "hcp_state":{"datatype": "str", "description": "Column name to use for Provider State"},
          "hcp_zip":{"datatype": "str", "description": "Column name to use for Provider Zip"},
          "dx_1":{"datatype": "str", "description": "Column name to use for Diagnosis Code 1"},
          "dx_2":{"datatype": "str", "description": "Column name to use for Diagnosis Code 2"},
          "referral_source":{"datatype": "str", "description": "Column name to use for Referral Source"},
          "cs_outlet_id":{"datatype": "str", "description": "Column name to use for CS Outlet ID"},
          "cot":{"datatype": "str", "description": "Column name to use for Class of Trade"},
          "hierarchy":{"datatype": "str", "description": "Column name to use for Hierarchy"},
          "active_status_code":{"datatype": "str", "description": "Active Shipment Status code, e.g. ACTIVE (customer-specific)"},
          "active_substatus_code":{"datatype": "str", "description": "Active Shipment Substatus code, e.g. SHIPMENT (customer-specific)"},
          "fulfillment_hierarchy":{"datatype": "str", "description": "Hierarchy used for statuses after the first fill, e.g. ACTIVE - SHIPMENT (customer-specific)"},
          "discontinued_hierarchy":{"datatype": "list", "description": "List of any hierarchies that we know should be excluded from TTFF"},
          "remove_from_ttff":{"datatype": "str", "description": ""Remove from TTFF" Hierarchy designation (customer-specific?)"},
          "input_transform":{"datatype": "str", "description": "The name of the dataset to pull from"}}',
      (SELECT id
      FROM pipeline_state_types
      WHERE name = 'ingest'),
      'jtobias@integrichain.com');
  COMMIT;