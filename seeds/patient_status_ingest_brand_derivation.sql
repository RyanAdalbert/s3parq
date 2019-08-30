BEGIN;
	INSERT INTO transformation_templates
		(name, variable_structures, pipeline_state_type_id, last_actor)
	VALUES
		('patient_status_ingest_brand_derivation',
		'{"input_transform":{"datatype": "str", "description": "Name of transform to fetch data from"}}',
		(SELECT id FROM pipeline_state_types WHERE name = 'ingest'),
		'njb@integrichain.com');
COMMIT;

BEGIN;
	INSERT INTO transformations
		(transformation_template_id, pipeline_state_id, graph_order, last_actor)
	VALUES
		((SELECT id FROM transformation_templates WHERE name = 'patient_status_ingest_brand_derivation'),
		(SELECT id FROM pipeline_states WHERE pipeline_state_type_id = (SELECT id FROM pipeline_state_types WHERE name = 'ingest') AND pipeline_id = (SELECT id FROM pipelines WHERE name = 'sun_allbrands_patient_status')),
		4,
		'njb@integrichain.com');
COMMIT;

BEGIN;
	INSERT INTO transformation_variables
		(name, transformation_id, value, last_actor)
	VALUES
		('input_transform',
		(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'sun_allbrands_patient_status')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'input_transform' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'patient_status_ingest_brand_derivation')))ORDER BY id LIMIT 1),
		'patient_status_standardize_dates',
		'njb@integrichain.com');
COMMIT;