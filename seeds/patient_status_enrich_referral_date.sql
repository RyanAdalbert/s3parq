BEGIN;
	INSERT INTO transformation_templates
		(name, variable_structures, pipeline_state_type_id, last_actor)
	VALUES
		('patient_status_enrich_referral_date',
		'{"input_transform":{"datatype": "str", "description": "Name of transform to fetch data from"},
			"threshold":{"datatype": "int", "description": "Maximum days to use in referral date enrichment"}}',
		(SELECT id FROM pipeline_state_types WHERE name = 'enrich'),
		'njb@integrichain.com');
COMMIT;

BEGIN;
	INSERT INTO transformations
		(transformation_template_id, pipeline_state_id, graph_order, last_actor)
	VALUES
		((SELECT id FROM transformation_templates WHERE name = 'patient_status_enrich_referral_date'),
		(SELECT id FROM pipeline_states WHERE pipeline_state_type_id = (SELECT id FROM pipeline_state_types WHERE name = 'enrich') AND pipeline_id = (SELECT id FROM pipelines WHERE name = 'alkermes_vivitrol_patient_status')),
		0,
		'njb@integrichain.com');
COMMIT;

BEGIN;
	INSERT INTO transformation_variables
		(name, transformation_id, value, last_actor)
	VALUES
		('input_transform',
		(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'alkermes_vivitrol_patient_status')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'input_transform' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'patient_status_enrich_referral_date')))ORDER BY id LIMIT 1),
		'alkermes_asembia_preprocessor',
		'njb@integrichain.com'),
		('threshold',
		(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'alkermes_vivitrol_patient_status')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'threshold' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'patient_status_enrich_referral_date')))ORDER BY id LIMIT 1),
		'60',
		'njb@integrichain.com');
COMMIT;