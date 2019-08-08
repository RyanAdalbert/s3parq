BEGIN;
INSERT INTO pipelines (name, is_active, description, pipeline_type_id, brand_id, run_frequency, last_actor)
    VALUES
        ('enrich_pending_too_long_test_pipeline', TRUE, 'Enrich Pending Too Long Test Pipeline', (SELECT id FROM pipeline_types WHERE name = 'patient_journey'), (SELECT id from brands WHERE name = 'ILUMYA'), 'weekly', 'jtobias@integrichain.com');

INSERT INTO transformation_templates (name, variable_structures, pipeline_state_type_id, last_actor) 
    VALUES
       ('enrich_pending_too_long', 
        '{"unique_id":{"datatype": "string", "description": "ID for ic_{id}_ptl modification"}, "trans_id":{"datatype": "str", "description": "Transaction ID"},    "brand_col":{"datatype": "str", "description": "Brand"},    "patient_id":{"datatype": "str", "description": "Patient ID"},      "pharmacy":{"datatype": "str", "description": "Pharmacy"},      "status_date":{"datatype": "str", "description": "status date"},    "referral_date":{"datatype": "str", "description": "Referral Date"},    "status":{"datatype": "str", "description": "Status"},      "substatus":{"datatype": "str", "description": "Substatus"},    "hierarchy":{"datatype": "str", "description": "Hierarchy"},    "pending_status_code":{"datatype": "str", "description": "Pending status code (customer-specific)"},    "cancel_status_code":{"datatype": "str", "description": "Cancel status code (customer-specific)"},      "pending_too_long_code":{"datatype": "str", "description": "Pending Too Long status code"},     "ptl_threshold":{"datatype": "int", "description": "Number of days threshold for inserting a PENDING TOO LONG record (customer-specific)"}}',
        (SELECT id FROM pipeline_state_types WHERE name = 'enrich'),
        'jtobias@integrichain.com');

INSERT INTO pipeline_states (pipeline_state_type_id, pipeline_id, graph_order, last_actor)
    VALUES 
        ((SELECT id FROM pipeline_state_types WHERE name = 'enrich'), (SELECT id FROM pipelines WHERE name = 'enrich_pending_too_long_test_pipeline'), 1, 'jtobias@integrichain.com');

INSERT INTO transformations (transformation_template_id, pipeline_state_id, graph_order, last_actor)
    VALUES
        ((SELECT id FROM transformation_templates WHERE name = 'extract_from_ftp'),(SELECT id FROM pipeline_states WHERE pipeline_state_type_id = (SELECT id FROM pipeline_state_types WHERE name = 'raw') AND pipeline_id = (SELECT id FROM pipelines WHERE name = 'enrich_pending_too_long_test_pipeline')), 0, 'jtobias@integrichain.com'),
        ((SELECT id FROM transformation_templates WHERE name = 'symphony_health_association_ingest_column_mapping'),(SELECT id FROM pipeline_states WHERE pipeline_state_type_id = (SELECT id FROM pipeline_state_types WHERE name = 'enrich') AND pipeline_id = (SELECT id FROM pipelines WHERE name = 'enrich_pending_too_long_test_pipeline')), 0, 'jtobias@integrichain.com'),
        ((SELECT id FROM transformation_templates WHERE name = 'enrich_pending_too_long'),(SELECT id FROM pipeline_states WHERE pipeline_state_type_id = (SELECT id FROM pipeline_state_types WHERE name = 'enrich') AND pipeline_id = (SELECT id FROM pipelines WHERE name = 'enrich_pending_too_long_test_pipeline')), 0, 'jtobias@integrichain.com');

INSERT INTO transformation_variables (name, transformation_id, value, last_actor)
    VALUES
        -- transformation variables for enrich_pending_too_long - sun ilumya
        ('unique_id',(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'sun_ilumya_extract')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'pharm_transaction_id' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'symphony_health_association_ingest_column_mapping')))ORDER BY id LIMIT 1), 'Pharm Transaction Id', 'jtobias@integrichain.com'),
        ('trans_id',(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'sun_ilumya_extract')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'pharm_transaction_id' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'symphony_health_association_ingest_column_mapping')))ORDER BY id LIMIT 1), 'Pharm Transaction Id', 'jtobias@integrichain.com'),
        ('brand_col',(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'sun_ilumya_extract')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'medication' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'symphony_health_association_ingest_column_mapping')))ORDER BY id LIMIT 1), 'Medication', 'jtobias@integrichain.com'),
        ('patient_id',(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'sun_ilumya_extract')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'msa_patient_id' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'symphony_health_association_ingest_column_mapping')))ORDER BY id LIMIT 1), 'MSA PATIENT ID', 'jtobias@integrichain.com'),
        ('pharmacy',(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'sun_ilumya_extract')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'pharm_code_col' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'symphony_health_association_ingest_column_mapping')))ORDER BY id LIMIT 1), 'Pharm Code', 'jtobias@integrichain.com'),
        ('status_date',(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'sun_ilumya_extract')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'status_date' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'symphony_health_association_ingest_column_mapping')))ORDER BY id LIMIT 1), 'Status Date', 'jtobias@integrichain.com'),
        ('referral_date',(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'sun_ilumya_extract')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'ref_date' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'symphony_health_association_ingest_column_mapping')))ORDER BY id LIMIT 1), 'Ref Date', 'njb@integrichain.com'),
        ('status',(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'sun_ilumya_extract')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'status_code' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'symphony_health_association_ingest_column_mapping')))ORDER BY id LIMIT 1), 'Status Code', 'njb@integrichain.com'),
        ('substatus',(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'sun_ilumya_extract')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'sub_status' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'symphony_health_association_ingest_column_mapping')))ORDER BY id LIMIT 1), 'Sub Status', 'njb@integrichain.com'),

COMMIT;