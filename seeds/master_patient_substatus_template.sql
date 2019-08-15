BEGIN;
INSERT INTO transformation_templates (name, variable_structures, pipeline_state_type_id, last_actor) 
    VALUES       
        ('master_patient_substatus', 
        '{"input_transform":{"datatype": "string", "description": "The name of the transform to input source data from"},"col_substatus":{"dataype": "string","description": "The column of interest for this transform"},"customer_name":{"datatype": "str", "description": "The customer name"}', 
        (SELECT id FROM pipeline_state_types WHERE name = 'master'),
        'jshea@integrichain.com');
COMMIT;
