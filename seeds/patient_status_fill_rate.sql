BEGIN;
  INSERT INTO transformation_templates
    (name, variable_structures, pipeline_state_type_id, last_actor)
  VALUES
    ('standardize_numbers',
    '{"ic_status":{"datatype": "string", "description": "column name of integrichain status"},"ic_sub_status":{"datatype": "string", "description": "column name of integrichain sub status"},"pjh":{"datatype": "string", "description": "column name of patient journey heirarchy"},"shipment_status":{"datatype": "string", "description": "string of shipment status. Should be something like "SHIPMENT""},"transfered_status":{"datatype": "string", "description": "string of transfered status. Should be something like "TRANSFERED""},"cancelled_status":{"datatype": "string", "description": "string of cancelled status. Should be something like "CANCELLED""},"open_status":{"datatype": "string", "description": "string of cancelled status. Should be something like "OPEN""},"filled_status":{"datatype": "string", "description": "string of cancelled status. Should be something like "FILLED""},"referral_status":{"datatype": "string", "description": "column name of referral status. Should be something like "referral_status""}}',
      (SELECT id
      FROM pipeline_state_types
      WHERE name = 'metrics'),
      'jlewis@integrichain.com');
  COMMIT;