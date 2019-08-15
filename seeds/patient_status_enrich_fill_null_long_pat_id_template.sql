BEGIN;
  INSERT INTO transformation_templates
    (name, variable_structures, pipeline_state_type_id, last_actor)
  VALUES
    ('patient_status_enrich_fill_null_long_pat_id',
      '{
          "brand_id":{"datatype": "str", "description": "This column is for the brand/medication. Used for identification purposes"},
          "pharma_code":{"datatype": "str", "description": "This column is the for the pharmacy code  Used for identification purposes"},
          "pharma_id":{"datatype": "str", "description": "This column is for the SP-ID.  Used for identification purposes and to fill in null values where there is no Long-ID"},
          "pat_id":{"datatype": "str", "description": "This column is for the Long-ID I.E. the column where null values are to be filled in"},
          "input_transform":{"datatype": "str", "description": "The name of the dataset to pull from"}}',
      (SELECT id
      FROM pipeline_state_types
      WHERE name = 'enrich'),
      'jtobias@integrichain.com');
  COMMIT;