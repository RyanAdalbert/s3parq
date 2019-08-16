BEGIN;
  INSERT INTO transformation_templates
    (name, variable_structures, pipeline_state_type_id, last_actor)
  VALUES
    ('patient_status_standardize_numbers',
      '{"input_transform":{"datatype": "string", "description": "The name of the transform to input source data from"}, 
          "number_columns":{"datatype": "string", "description": "Columns in our dataframe which need to be converted to numbers.  Should be comma-separated string with no spaces"}}',
      (SELECT id
      FROM pipeline_state_types
      WHERE name = 'ingest'),
      'jtobias@integrichain.com');
  COMMIT;