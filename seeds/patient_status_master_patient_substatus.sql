BEGIN;
	INSERT INTO transformation_templates
		(name, variable_structures, pipeline_state_type_id, last_actor)
	VALUES
		('master_patient_substatus',
		'{"input_transform":{"datatype": "str", "description": "Name of transform to fetch data from"},
			"col_substatus":{"datatype": "string", "description": "Column of interest for the transformation"},
			"col_customer_name":{"datatype": "string", "description": "the customer name"}}',
		(SELECT id FROM pipeline_state_types WHERE name = 'master'),
		'njb@integrichain.com');
COMMIT;

BEGIN;
	INSERT INTO transformations
		(transformation_template_id, pipeline_state_id, graph_order, last_actor)
	VALUES
		((SELECT id FROM transformation_templates WHERE name = 'master_patient_substatus'),
		(SELECT id FROM pipeline_states WHERE pipeline_state_type_id = (SELECT id FROM pipeline_state_types WHERE name = 'master') AND pipeline_id = (SELECT id FROM pipelines WHERE name = 'sun_all_brands_patient_status')),
		1,
		'njb@integrichain.com'),
		((SELECT id FROM transformation_templates WHERE name = 'master_patient_substatus'),
		(SELECT id FROM pipeline_states WHERE pipeline_state_type_id = (SELECT id FROM pipeline_state_types WHERE name = 'master') AND pipeline_id = (SELECT id FROM pipelines WHERE name = 'alkermes_vivitrol_patient_status')),
		1,
		'njb@integrichain.com'),
		((SELECT id FROM transformation_templates WHERE name = 'master_patient_substatus'),
		(SELECT id FROM pipeline_states WHERE pipeline_state_type_id = (SELECT id FROM pipeline_state_types WHERE name = 'master') AND pipeline_id = (SELECT id FROM pipelines WHERE name = 'alkermes_vivitrol_patient_status_asembia')),
		1,
		'njb@integrichain.com');
COMMIT;

BEGIN;
	INSERT INTO transformation_variables
		(name, transformation_id, value, last_actor)
	VALUES
		('input_transform',
		(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'sun_all_brands_patient_status')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'input_transform' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'master_patient_substatus')))ORDER BY id LIMIT 1),
		'master_patient_status',
		'njb@integrichain.com'),
		('col_substatus',
		(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'sun_all_brands_patient_status')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'col_substatus' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'master_patient_substatus')))ORDER BY id LIMIT 1),
		'customer_substatus',
		'njb@integrichain.com'),
		('col_customer_name',
		(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'sun_all_brands_patient_status')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'col_customer_name' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'master_patient_substatus')))ORDER BY id LIMIT 1),
		'sun',
		'njb@integrichain.com'),
		('input_transform',
		(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'alkermes_vivitrol_patient_status')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'input_transform' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'master_patient_substatus')))ORDER BY id LIMIT 1),
		'master_patient_status',
		'njb@integrichain.com'),
		('col_substatus',
		(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'alkermes_vivitrol_patient_status')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'col_substatus' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'master_patient_substatus')))ORDER BY id LIMIT 1),
		'customer_substatus',
		'njb@integrichain.com'),
		('col_customer_name',
		(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'alkermes_vivitrol_patient_status')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'col_customer_name' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'master_patient_substatus')))ORDER BY id LIMIT 1),
		'alkermes',
		'njb@integrichain.com'),
		('input_transform',
		(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'alkermes_vivitrol_patient_status_asembia')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'input_transform' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'master_patient_substatus')))ORDER BY id LIMIT 1),
		'master_patient_status',
		'njb@integrichain.com'),
		('col_substatus',
		(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'alkermes_vivitrol_patient_status_asembia')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'col_substatus' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'master_patient_substatus')))ORDER BY id LIMIT 1),
		'customer_substatus',
		'njb@integrichain.com'),
		('col_customer_name',
		(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'alkermes_vivitrol_patient_status_asembia')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'col_customer_name' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'master_patient_substatus')))ORDER BY id LIMIT 1),
		'alkermes',
		'njb@integrichain.com');
COMMIT;
