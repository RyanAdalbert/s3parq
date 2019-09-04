BEGIN;
	INSERT INTO transformation_templates
		(name, variable_structures, pipeline_state_type_id, last_actor)
	VALUES
		('patient_status_enrich_pending_too_long',
		'{"input_transform":{"datatype": "string", "description": "Name of transform to fetch data from"},
			"pending_status_code":{"datatype": "string", "description": "Pending status code (customer-specific)"},
			"cancel_status_code":{"datatype": "string", "description": "Cancel status code (customer-specific)"},
			"pending_too_long_code":{"datatype": "string", "description": "Pending Too Long status code"},
			"ptl_threshold":{"datatype": "int", "description": "Number of days threshold for inserting a PENDING TOO LONG record (customer-specific)"},
		(SELECT id FROM pipeline_state_types WHERE name = 'enrich'),
		'jlewis@integrichain.com');
COMMIT;

BEGIN;
	INSERT INTO transformations
		(transformation_template_id, pipeline_state_id, graph_order, last_actor)
	VALUES
		((SELECT id FROM transformation_templates WHERE name = 'patient_status_enrich_pending_too_long'),
		(SELECT id FROM pipeline_states WHERE pipeline_state_type_id = (SELECT id FROM pipeline_state_types WHERE name = 'enrich') AND pipeline_id = (SELECT id FROM pipelines WHERE name = 'alkermes_vivitrol_patient_status')),
		9,
		'jlewis@integrichain.com');
COMMIT;

BEGIN;
	INSERT INTO transformation_variables
		(name, transformation_id, value, last_actor)
	VALUES
		('input_transform',
		(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'alkermes_vivitrol_patient_status')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'input_transform' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'patient_status_enrich_pending_too_long')))ORDER BY id LIMIT 1),
		'patient_status_enrich_cancel_not_before_active',
		'jlewis@integrichain.com'),
		('pending_status_code',
		(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'alkermes_vivitrol_patient_status')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'pending_status_code' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'patient_status_enrich_pending_too_long')))ORDER BY id LIMIT 1),
		'PENDING',
		'jlewis@integrichain.com'),
		('cancel_status_code',
		(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'alkermes_vivitrol_patient_status')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'cancel_status_code' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'patient_status_enrich_pending_too_long')))ORDER BY id LIMIT 1),
		'CANCELLED',
		'jlewis@integrichain.com'),
		('pending_too_long_code',
		(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'alkermes_vivitrol_patient_status')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'pending_too_long_code' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'patient_status_enrich_pending_too_long')))ORDER BY id LIMIT 1),
		'PENDING TOO LONG',
		'jlewis@integrichain.com'),
		('ptl_threshold',
		(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'alkermes_vivitrol_patient_status')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'ptl_threshold' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'patient_status_enrich_pending_too_long')))ORDER BY id LIMIT 1),
		'60',
		'jlewis@integrichain.com');
COMMIT;
