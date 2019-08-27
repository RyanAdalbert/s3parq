BEGIN;
INSERT INTO transformation_templates (name, variable_structures, pipeline_state_type_id, last_actor) 
    VALUES       
        ('patient_status_enrich_patient_journey_hierarchy', 
        '{
            "col_status":{"datatype": "str", "description": "Column containing the status"},
            "col_substatus":{"datatype": "str", "description": "Column containing the substatus"},
            "customer_name":{"datatype": "str", "description": "Name of pharmaceutical company"},
            "input_transform":{"datatype": "str", "description": "The name of the dataset to pull from"}}', 
        (SELECT id FROM pipeline_state_types WHERE name = 'enrich'),
        'jtobias@integrichain.com');
COMMIT;