BEGIN;
INSERT INTO transformation_templates (name, variable_structures, pipeline_state_type_id, last_actor) 
    VALUES       
        ('master_patient_primary_benefit_type', 
        '{"input_transform":{"datatype": "string", "description": "The name of the transform to input source data from"}}', 
        (SELECT id FROM pipeline_state_types WHERE name = 'master'),
        'njb@integrichain.com');
COMMIT;