BEGIN;
	INSERT INTO transformation_templates
		(name, variable_structures, pipeline_state_type_id, last_actor)
	VALUES
		('patient_status_enrich_fill_null_long_pat_id',
		'{"brand_id":{"datatype": "str", "description": "This column is for the brand/medication. Used for identification purposes"},
			"pharma_code":{"datatype": "str", "description": "This column is the for the pharmacy code  Used for identification purposes"},
			"pharma_id":{"datatype": "str", "description": "This column is for the SP-ID.  Used for identification purposes and to fill in null values where there is no Long-ID"},
			"pat_id":{"datatype": "str", "description": "This column is for the Long-ID I.E. the column where null values are to be filled in"},
			"input_transform":{"datatype": "str", "description": "The name of the dataset to pull from"}}',
		(SELECT id FROM pipeline_state_types WHERE name = 'enrich'),
		'njb@integrichain.com');
COMMIT;

BEGIN;
	INSERT INTO transformations
		(transformation_template_id, pipeline_state_id, graph_order, last_actor)
	VALUES
		((SELECT id FROM transformation_templates WHERE name = 'patient_status_enrich_fill_null_long_pat_id'),
		(SELECT id FROM pipeline_states WHERE pipeline_state_type_id = (SELECT id FROM pipeline_state_types WHERE name = 'enrich') AND pipeline_id = (SELECT id FROM pipelines WHERE name = 'sun_allbrands_patient_status')),
		1,
		'njb@integrichain.com');
COMMIT;

BEGIN;
	INSERT INTO transformation_variables
		(name, transformation_id, value, last_actor)
	VALUES
		('brand_id',
		(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'sun_allbrands_patient_status')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'brand_id' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'patient_status_enrich_fill_null_long_pat_id')))ORDER BY id LIMIT 1),
		'medication',
		'njb@integrichain.com'),
		('pharma_code',
		(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'sun_allbrands_patient_status')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'pharma_code' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'patient_status_enrich_fill_null_long_pat_id')))ORDER BY id LIMIT 1),
		'pharmacy_code',
		'njb@integrichain.com'),
		('pharma_id',
		(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'sun_allbrands_patient_status')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'pharma_id' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'patient_status_enrich_fill_null_long_pat_id')))ORDER BY id LIMIT 1),
		'pharmacy_patient_id',
		'njb@integrichain.com'),
		('pat_id',
		(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'sun_allbrands_patient_status')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'pat_id' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'patient_status_enrich_fill_null_long_pat_id')))ORDER BY id LIMIT 1),
		'longitudinal_patient_id',
		'njb@integrichain.com'),
		('input_transform',
		(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'sun_allbrands_patient_status')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'input_transform' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'patient_status_enrich_fill_null_long_pat_id')))ORDER BY id LIMIT 1),
		'patient_status_enrich_patient_journey_hierarchy',
		'njb@integrichain.com');
COMMIT;