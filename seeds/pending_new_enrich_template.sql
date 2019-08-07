BEGIN;
INSERT INTO pipelines (name, is_active, description, pipeline_type_id, brand_id, run_frequency, last_actor)
    VALUES
        ('pending_new_enrich_test_pipeline', TRUE, 'Pending New Enrich Test Pipeline', (SELECT id FROM pipeline_types WHERE name = 'patient_journey'), (SELECT id from brands WHERE name = 'ILUMYA'), 'weekly', 'jtobias@integrichain.com');

INSERT INTO transformation_templates (name, variable_structures, pipeline_state_type_id, last_actor) 
    VALUES
       ('pending_new_enrich', 
        '{"input_transform":{"datatype": "string", "description": "The name of the transform to input source data from"}, "trans_id":{"datatype": "str", "description": "transaction id"},"    product":{"datatype": "str", "description": "product"},"    patient":{"datatype": "str", "description": "patient id"},"    pharm":{"datatype": "str", "description": "pharmacy name"},"    status_date":{"datatype": "str", "description": "status date"},"    ref_date":{"datatype": "str", "description": "ref date"},"    status":{"datatype": "str", "description": "status"},"    substatus":{"datatype": "str", "description": "substatus"},"    ic_status":{"datatype": "str", "description": "ic_status"},"    ic_substatus":{"datatype": "str", "description": "ic_substatus"},"    pending_status":{"datatype": "str", "description": "pending_status"},"    active_status":{"datatype": "str", "description": "active_status"},"    cancelled_status":{"datatype": "str", "description": "cancelled_status"},"    pending_new_substatus":{"datatype": "str", "description": "pending_new_substatus"},"  ":{"datatype": "   ", "description": ""}}',
        (SELECT id FROM pipeline_state_types WHERE name = 'enrich'),
        'jtobias@integrichain.com'),
       ('referral_date_enrich', 
        '{"input_transform":{"datatype": "string", "description": "The name of the transform to input source data from"}, "trans_id":{"datatype": "str", "description": "description of trans_id"},"product":{"datatype": "str", "description": "description of product"},"patient":{"datatype": "str", "description": "description of patient"},"pharm":{"datatype": "str", "description": "description of pharm"},"status_date":{"datatype": "str", "description": "description of status_date"},"ref_date":{"datatype": "str", "description": "description of ref_date"},"status":{"datatype": "str", "description": "description of status"},"substatus":{"datatype": "str", "description": "description of substatu"}}',
        (SELECT id FROM pipeline_state_types WHERE name = 'enrich'),
        'jtobias@integrichain.com');


INSERT INTO pipeline_states (pipeline_state_type_id, pipeline_id, graph_order, last_actor)
    VALUES 
        ((SELECT id FROM pipeline_state_types WHERE name = 'raw'), (SELECT id FROM pipelines WHERE name = 'pending_new_enrich_test_pipeline'), 0, 'jtobias@integrichain.com'),
        ((SELECT id FROM pipeline_state_types WHERE name = 'enrich'), (SELECT id FROM pipelines WHERE name = 'pending_new_enrich_test_pipeline'), 1, 'jtobias@integrichain.com');

COMMIT;

BEGIN;
INSERT INTO transformations (transformation_template_id, pipeline_state_id, graph_order, last_actor)
    VALUES
        ((SELECT id FROM transformation_templates WHERE name = 'extract_from_ftp'),(SELECT id FROM pipeline_states WHERE pipeline_state_type_id = (SELECT id FROM pipeline_state_types WHERE name = 'raw') AND pipeline_id = (SELECT id FROM pipelines WHERE name = 'pending_new_enrich_test_pipeline')), 0, 'jtobias@integrichain.com'),
        ((SELECT id FROM transformation_templates WHERE name = 'pending_new_enrich'),(SELECT id FROM pipeline_states WHERE pipeline_state_type_id = (SELECT id FROM pipeline_state_types WHERE name = 'enrich') AND pipeline_id = (SELECT id FROM pipelines WHERE name = 'pending_new_enrich_test_pipeline')), 0, 'jtobias@integrichain.com'),
        ((SELECT id FROM transformation_templates WHERE name = 'referral_date_enrich'),(SELECT id FROM pipeline_states WHERE pipeline_state_type_id = (SELECT id FROM pipeline_state_types WHERE name = 'enrich') AND pipeline_id = (SELECT id FROM pipelines WHERE name = 'pending_new_enrich_test_pipeline')), 1, 'jtobias@integrichain.com');
COMMIT;

