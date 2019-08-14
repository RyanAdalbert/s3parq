BEGIN;
  INSERT INTO transformation_templates
    (name, variable_structures, pipeline_state_type_id, last_actor)
  VALUES
    ('patient_status_fill_rate',
    '{"input_transform":{"datatype": "string", "description": "The name of the transform to input source data from"},"shipment_status":{"datatype": "string", "description": "String of shipment status. Should be something like "SHIPMENT""},"transfered_status":{"datatype": "string", "description": "String of transfered status. Should be something like "TRANSFERED""},"cancelled_status":{"datatype": "string", "description": "String of cancelled status. Should be something like "CANCELLED""},"open_status":{"datatype": "string", "description": "String of cancelled status. Should be something like "OPEN""},"filled_status":{"datatype": "string", "description": "String of cancelled status. Should be something like "FILLED""}}',
      (SELECT id
      FROM pipeline_state_types
      WHERE name = 'metrics'),
      'jlewis@integrichain.com');
  COMMIT;