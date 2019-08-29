BEGIN;
	INSERT INTO transformation_templates
		(name, variable_structures, pipeline_state_type_id, last_actor)
	VALUES
		('enrich_active_shipment',
		'{"input_transform":{"datatype": "string", "description": "The name of the transform to input source data from"},
			"dispense_input_transform":{"datatype": "string", "description": "The name of the transform to input dispense data from"},
			"unique_id":{"datatype": "string", "description": "Column name to use as ID for ic_{id}_ptl modification"},
			"trans_id":{"datatype": "string", "description": "Column name to use for Transaction ID"},
			"brand_col":{"datatype": "string", "description": "Column name to use for Brand"},
			"patient_id":{"datatype": "string", "description": "Column name to use for Patient ID"},
			"pharmacy":{"datatype": "string", "description": "Column name to use for Pharmacy"},
			"status_date":{"datatype": "string", "description": "Column name to use for Status Date"},
			"referral_date":{"datatype": "string", "description": "Column name to use for Referral Date"},
			"status":{"datatype": "string", "description": "Column name to use for Status"},
			"substatus":{"datatype": "string", "description": "Column name to use for Substatus"},
			"hierarchy":{"datatype": "string", "description": "Column name to use for Hierarchy"},
			"dispense_status_date":{"datatype": "string", "description": "Dispense column name to use for Status Date"},
			"dispense_datetime":{"datatype": "string", "description": "Datetime format found in the Dispense data"},
			"brand_name":{"datatype": "string", "description": "Name of brand to be inserted into brand column of Dispense data"},
			"active_shipment_status":{"datatype": "string", "description": "Status indicating active shipment (customer-specific)"},
			"active_shipment_substatus":{"datatype": "string", "description": "Substatus indicating active shipment (customer-specific)"},
			"active_hierarchy":{"datatype": "string", "description": "Hierarchy indicating active shipment (customer-specific)"},
			"pharmacy_name_map":{"datatype": "string", "description": "Dictionary with pharmacy names found in Dispense data to be mapped to standardized names, e.g. {'CVS':'CVS Specialty'} (customer-specific)"}}',
		(SELECT id FROM pipeline_state_types WHERE name = 'enrich'),
		'hjz@integrichain.com');
COMMIT;

BEGIN;
	INSERT INTO transformations
		(transformation_template_id, pipeline_state_id, graph_order, last_actor)
	VALUES
		((SELECT id FROM transformation_templates WHERE name = 'enrich_active_shipment'),
		(SELECT id FROM pipeline_states WHERE pipeline_state_type_id = (SELECT id FROM pipeline_state_types WHERE name = 'enrich') AND pipeline_id = (SELECT id FROM pipelines WHERE name = 'alkermes_vivitrol_patient_status')),
		1,
		'hjz@integrichain.com');
COMMIT;

BEGIN;
	INSERT INTO transformation_variables
		(name, transformation_id, value, last_actor)
	VALUES
		('input_transform',
		(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'alkermes_vivitrol_patient_status')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'input_transform' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'enrich_active_shipment')))ORDER BY id LIMIT 1),
		'patient_status_enrich_referral_date',
		'hjz@integrichain.com'),
		('dispense_input_transform',
		(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'alkermes_vivitrol_patient_status')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'dispense_input_transform' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'enrich_active_shipment')))ORDER BY id LIMIT 1),
		'dispense_ingest_column_mapping',
		'hjz@integrichain.com'),
		('unique_id',
		(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'alkermes_vivitrol_patient_status')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'unique_id' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'enrich_active_shipment')))ORDER BY id LIMIT 1),
		'aggregator_transaction_id',
		'hjz@integrichain.com'),
		('trans_id',
		(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'alkermes_vivitrol_patient_status')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'trans_id' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'enrich_active_shipment')))ORDER BY id LIMIT 1),
		'aggregator_transaction_id',
		'hjz@integrichain.com'),
		('brand_col',
		(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'alkermes_vivitrol_patient_status')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'brand_col' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'enrich_active_shipment')))ORDER BY id LIMIT 1),
		'brand',
		'hjz@integrichain.com'),
		('patient_id',
		(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'alkermes_vivitrol_patient_status')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'patient_id' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'enrich_active_shipment')))ORDER BY id LIMIT 1),
		'longitudinal_patient_id',
		'hjz@integrichain.com'),
		('pharmacy',
		(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'alkermes_vivitrol_patient_status')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'pharmacy' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'enrich_active_shipment')))ORDER BY id LIMIT 1),
		'pharmacy_name',
		'hjz@integrichain.com'),
		('status_date',
		(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'alkermes_vivitrol_patient_status')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'status_date' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'enrich_active_shipment')))ORDER BY id LIMIT 1),
		'status_date',
		'hjz@integrichain.com'),
		('referral_date',
		(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'alkermes_vivitrol_patient_status')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'referral_date' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'enrich_active_shipment')))ORDER BY id LIMIT 1),
		'referral_date',
		'hjz@integrichain.com'),
		('status',
		(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'alkermes_vivitrol_patient_status')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'status' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'enrich_active_shipment')))ORDER BY id LIMIT 1),
		'customer_status',
		'hjz@integrichain.com'),
		('substatus',
		(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'alkermes_vivitrol_patient_status')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'substatus' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'enrich_active_shipment')))ORDER BY id LIMIT 1),
		'customer_substatus',
		'hjz@integrichain.com'),
		('hierarchy',
		(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'alkermes_vivitrol_patient_status')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'hierarchy' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'enrich_active_shipment')))ORDER BY id LIMIT 1),
		'hierarchy',
		'hjz@integrichain.com'),
		('dispense_status_date',
		(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'alkermes_vivitrol_patient_status')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'dispense_status_date' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'enrich_active_shipment')))ORDER BY id LIMIT 1),
		'ship_date',
		'hjz@integrichain.com'),
		('dispense_datetime',
		(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'alkermes_vivitrol_patient_status')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'dispense_datetime' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'enrich_active_shipment')))ORDER BY id LIMIT 1),
		'%Y%m%d',
		'hjz@integrichain.com'),
		('brand_name',
		(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'alkermes_vivitrol_patient_status')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'brand_name' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'enrich_active_shipment')))ORDER BY id LIMIT 1),
		'VIVITROL',
		'hjz@integrichain.com'),
		('active_shipment_status',
		(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'alkermes_vivitrol_patient_status')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'active_shipment_status' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'enrich_active_shipment')))ORDER BY id LIMIT 1),
		'ACTIVE',
		'hjz@integrichain.com'),
		('active_shipment_substatus',
		(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'alkermes_vivitrol_patient_status')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'active_shipment_substatus' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'enrich_active_shipment')))ORDER BY id LIMIT 1),
		'AS01',
		'hjz@integrichain.com'),
		('active_hierarchy',
		(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'alkermes_vivitrol_patient_status')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'active_hierarchy' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'enrich_active_shipment')))ORDER BY id LIMIT 1),
		'FULFILLMENT',
		'hjz@integrichain.com'),
		('pharmacy_name_map',
		(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'alkermes_vivitrol_patient_status')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'pharmacy_name_map' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'enrich_active_shipment')))ORDER BY id LIMIT 1),
		'{"CVS":"CVS Specialty"}',
		'hjz@integrichain.com');
COMMIT;
