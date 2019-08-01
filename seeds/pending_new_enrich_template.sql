BEGIN;
INSERT INTO pipelines (name, is_active, description, pipeline_type_id, brand_id, run_frequency, last_actor)
    VALUES
        ('ike_jacob_test_pipeline', TRUE, 'Ike Jacob Test Pipeline -- ILUMYA', (SELECT id FROM pipeline_types WHERE name = 'patient_journey'), (SELECT id from brands WHERE name = 'ILUMYA'), 'weekly', 'jtobias@integrichain.com');

INSERT INTO transformation_templates (name, variable_structures, pipeline_state_type_id, last_actor) 
    VALUES
       ('pending_new_enrich', 
        '{"    trans_id":{"datatype": "str", "description": "transaction id"},"    product":{"datatype": "str", "description": "product"},"    patient":{"datatype": "str", "description": "patient id"},"    pharm":{"datatype": "str", "description": "pharmacy name"},"    status_date":{"datatype": "str", "description": "status date"},"    ref_date":{"datatype": "str", "description": "ref date"},"    status":{"datatype": "str", "description": "status"},"    substatus":{"datatype": "str", "description": "substatus"},"    ic_status":{"datatype": "str", "description": "ic_status"},"    ic_substatus":{"datatype": "str", "description": "ic_substatus"},"    pending_status":{"datatype": "str", "description": "pending_status"},"    active_status":{"datatype": "str", "description": "active_status"},"    cancelled_status":{"datatype": "str", "description": "cancelled_status"},"    pending_new_substatus":{"datatype": "str", "description": "pending_new_substatus"},"  ":{"datatype": "   ", "description": ""}}',
        (SELECT id FROM pipeline_state_types WHERE name = 'enrich'),
        'jtobias@integrichain.com'),