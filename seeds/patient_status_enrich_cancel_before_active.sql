BEGIN;
INSERT INTO transformation_templates (name, variable_structures, pipeline_state_type_id, last_actor)
    VALUES
        ('patient_status_enrich_cancel_before_active',
        '{"input_transform":{"datatype": "string","description": "Transform to source data from"},"active_substatus_code":{"datatype": "string","description": "Active Shipment Substatus code, e.g. SHIPMENT (customer-specific)"},"cancel_discontinue_status_code":{"datatype": "string","description": "List of Cancelled and Discontinued status codes (customer-specific)"},"bvpa_cancel_discontinue_substatus":{"datatype": "string","description": "List of accepted substatus codes used for BVPA hierarchy, e.g. [INSURANCE DENIED,COVERAGE DENIED] (customer-specific)"},"active_diff_threshold":{"datatype": "string","description": "Threshold value for Active/Cancel date difference logic (customer-specific)"},"prior_diff_threshold":{"datatype": "string","description": "Threshold value for Cancel/Prior date difference logic (customer-specific)"},"active_hierarchy":{"datatype": "string","description": "Hierarchy to assign to statuses after the first fill, e.g. ACTIVE - SHIPMENT (customer-specific)"},"remove_from_ttff":{"datatype": "string","description": "Hierarchy to assign to statuses that are ignored from TTFF (customer-specific)"},"no_status_clarity":{"datatype": "string","description": "Hierarchy to assign to cancelled/discontinued statuses with no status clarity (customer-specific)"},"bvpa_hierarchy":{"datatype": "string","description": "Hierarchy to assign to cancelled/discontinued statuses that have BVPA substatus (customer-specific)"},"hierarchy":{"datatype": "string","description": "Column name to use for Hierarchy"}}',
        (SELECT id FROM pipeline_state_types WHERE name = 'enrich'),
        'rns@integrichain.com');

COMMIT;

BEGIN;
INSERT INTO transformations (transformation_template_id, pipeline_state_id, graph_order, last_actor)
    VALUES
        ((SELECT id FROM transformation_templates WHERE name = 'patient_status_enrich_cancel_before_active'),(SELECT id FROM pipeline_states WHERE pipeline_state_type_id = (SELECT id FROM pipeline_state_types WHERE name = 'enrich') AND pipeline_id = (SELECT id FROM pipelines WHERE name = 'alkermes_vivitrol_patient_status')), 5, 'rns@integrichain.com');
COMMIT;

BEGIN;
INSERT INTO transformation_variables (name, transformation_id, value, last_actor)
    VALUES
        ('input_transform',(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'alkermes_vivitrol_patient_status')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'input_transform' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'patient_status_enrich_cancel_before_active')))ORDER BY id LIMIT 1), 'patient_status_enrich_pending_sequences', 'rns@integrichain.com'),
        ('active_substatus_code',(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'alkermes_vivitrol_patient_status')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'active_substatus_code' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'patient_status_enrich_cancel_before_active')))ORDER BY id LIMIT 1), 'SHIPMENT', 'rns@integrichain.com'),
        ('cancel_discontinue_status_code',(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'alkermes_vivitrol_patient_status')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'cancel_discontinue_status_code' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'patient_status_enrich_cancel_before_active')))ORDER BY id LIMIT 1), 'CANCELLED,DISCONTINUED', 'rns@integrichain.com'),
        ('bvpa_cancel_discontinue_substatus',(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'alkermes_vivitrol_patient_status')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'bvpa_cancel_discontinue_substatus' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'patient_status_enrich_cancel_before_active')))ORDER BY id LIMIT 1), 'INSURANCE DENIED', 'rns@integrichain.com'),
        ('active_diff_threshold',(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'alkermes_vivitrol_patient_status')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'active_diff_threshold' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'patient_status_enrich_cancel_before_active')))ORDER BY id LIMIT 1), '60', 'rns@integrichain.com'),
        ('prior_diff_threshold',(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'alkermes_vivitrol_patient_status')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'prior_diff_threshold' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'patient_status_enrich_cancel_before_active')))ORDER BY id LIMIT 1), '60', 'rns@integrichain.com'),
        ('active_hierarchy',(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'alkermes_vivitrol_patient_status')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'active_hierarchy' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'patient_status_enrich_cancel_before_active')))ORDER BY id LIMIT 1), 'ACTIVE - S01', 'rns@integrichain.com'),
        ('remove_from_ttff',(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'alkermes_vivitrol_patient_status')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'remove_from_ttff' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'patient_status_enrich_cancel_before_active')))ORDER BY id LIMIT 1), 'REMOVE FROM TTFF', 'rns@integrichain.com'),
        ('no_status_clarity',(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'alkermes_vivitrol_patient_status')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'no_status_clarity' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'patient_status_enrich_cancel_before_active')))ORDER BY id LIMIT 1), 'NO STATUS CLARITY', 'rns@integrichain.com'),
        ('bvpa_hierarchy',(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'alkermes_vivitrol_patient_status')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'bvpa_hierarchy' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'patient_status_enrich_cancel_before_active')))ORDER BY id LIMIT 1), 'BVPA', 'rns@integrichain.com'),
        ('hierarchy',(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'alkermes_vivitrol_patient_status')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'hierarchy' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'patient_status_enrich_cancel_before_active')))ORDER BY id LIMIT 1), 'nan', 'rns@integrichain.com');
COMMIT;