BEGIN;
	INSERT INTO transformation_templates
		(name, variable_structures, pipeline_state_type_id, last_actor)
	VALUES
		('patient_status_standardize_numbers',
		'{"input_transform":{"datatype": "string", "description": "Name of transform to fetch data from"},
			"number_columns":{"datatype": "string", "description": "Columns in our dataframe which need to be converted to numbers. Should be comma-separated string with no spaces"}}',
		(SELECT id FROM pipeline_state_types WHERE name = 'ingest'),
		'njb@integrichain.com');
COMMIT;

BEGIN;
	INSERT INTO transformations
		(transformation_template_id, pipeline_state_id, graph_order, last_actor)
	VALUES
		((SELECT id FROM transformation_templates WHERE name = 'patient_status_standardize_numbers'),
		(SELECT id FROM pipeline_states WHERE pipeline_state_type_id = (SELECT id FROM pipeline_state_types WHERE name = 'ingest') AND pipeline_id = (SELECT id FROM pipelines WHERE name = 'sun_all_brands_patient_status')),
		2,
		'njb@integrichain.com'),
		((SELECT id FROM transformation_templates WHERE name = 'patient_status_standardize_numbers'),
		(SELECT id FROM pipeline_states WHERE pipeline_state_type_id = (SELECT id FROM pipeline_state_types WHERE name = 'ingest') AND pipeline_id = (SELECT id FROM pipelines WHERE name = 'bi_ofev_patient_status')),
		2,
		'njb@integrichain.com'),
		((SELECT id FROM transformation_templates WHERE name = 'patient_status_standardize_numbers'),
		(SELECT id FROM pipeline_states WHERE pipeline_state_type_id = (SELECT id FROM pipeline_state_types WHERE name = 'ingest') AND pipeline_id = (SELECT id FROM pipelines WHERE name = 'alkermes_vivitrol_patient_status')),
		2,
		'njb@integrichain.com'),
		((SELECT id FROM transformation_templates WHERE name = 'patient_status_standardize_numbers'),
		(SELECT id FROM pipeline_states WHERE pipeline_state_type_id = (SELECT id FROM pipeline_state_types WHERE name = 'ingest') AND pipeline_id = (SELECT id FROM pipelines WHERE name = 'alkermes_vivitrol_patient_status_asembia')),
		2,
		'njb@integrichain.com');
COMMIT;

BEGIN;
	INSERT INTO transformation_variables
		(name, transformation_id, value, last_actor)
	VALUES
		('input_transform',
		(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'sun_all_brands_patient_status')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'input_transform' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'patient_status_standardize_numbers')))ORDER BY id LIMIT 1),
		'patient_status_ingest_column_mapping',
		'njb@integrichain.com'),
		('number_columns',
		(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'sun_all_brands_patient_status')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'number_columns' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'patient_status_standardize_numbers')))ORDER BY id LIMIT 1),
		'pharmacy_npi,pharmacy_ncpdp,pharmacy_zip,transaction_id,transaction_sequence,longitudinal_patient_id,patient_zip,hcp_zip,hcp_phone,hcp_npi,rx_fills,rx_fill_number,rx_refills_remaining,prev_dispensed,ndc,days_supply,ship_zip,primary_payer_bin,primary_payer_iin,primary_payer_pcn,secondary_payer_bin,secondary_payer_iin,secondary_payer_pcn,aggregator_ship_id,referral_number,primary_plan_paid,secondary_plan_paid,primary_copay,primary_coins,primary_deductible,primary_patient_responsibility,secondary_copay,secondary_coins,secondary_deductible,secondary_patient_responsibility,copay_as_amount,other_payer_amount,primary_cost_amount',
		'njb@integrichain.com'),
		('input_transform',
		(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'bi_ofev_patient_status')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'input_transform' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'patient_status_standardize_numbers')))ORDER BY id LIMIT 1),
		'patient_status_ingest_column_mapping',
		'njb@integrichain.com'),
		('number_columns',
		(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'bi_ofev_patient_status')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'number_columns' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'patient_status_standardize_numbers')))ORDER BY id LIMIT 1),
		'pharmacy_npi,pharmacy_ncpdp,pharmacy_zip,transaction_id,transaction_sequence,longitudinal_patient_id,patient_zip,hcp_zip,hcp_phone,hcp_npi,rx_fills,rx_fill_number,rx_refills_remaining,prev_dispensed,ndc,days_supply,ship_zip,primary_payer_bin,primary_payer_iin,primary_payer_pcn,secondary_payer_bin,secondary_payer_iin,secondary_payer_pcn,aggregator_ship_id,referral_number,primary_plan_paid,secondary_plan_paid,primary_copay,primary_coins,primary_deductible,primary_patient_responsibility,secondary_copay,secondary_coins,secondary_deductible,secondary_patient_responsibility,copay_as_amount,other_payer_amount,primary_cost_amount',
		'njb@integrichain.com'),
		('input_transform',
		(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'alkermes_vivitrol_patient_status')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'input_transform' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'patient_status_standardize_numbers')))ORDER BY id LIMIT 1),
		'patient_status_ingest_column_mapping',
		'njb@integrichain.com'),
		('number_columns',
		(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'alkermes_vivitrol_patient_status')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'number_columns' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'patient_status_standardize_numbers')))ORDER BY id LIMIT 1),
		'pharmacy_npi,pharmacy_ncpdp,pharmacy_zip,transaction_id,transaction_sequence,longitudinal_patient_id,patient_zip,hcp_zip,hcp_phone,hcp_npi,rx_fills,rx_fill_number,rx_refills_remaining,prev_dispensed,ndc,days_supply,ship_zip,primary_payer_bin,primary_payer_iin,primary_payer_pcn,secondary_payer_bin,secondary_payer_iin,secondary_payer_pcn,aggregator_ship_id,referral_number,primary_plan_paid,secondary_plan_paid,primary_copay,primary_coins,primary_deductible,primary_patient_responsibility,secondary_copay,secondary_coins,secondary_deductible,secondary_patient_responsibility,copay_as_amount,other_payer_amount,primary_cost_amount',
		'njb@integrichain.com'),
		('input_transform',
		(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'alkermes_vivitrol_patient_status_asembia')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'input_transform' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'patient_status_standardize_numbers')))ORDER BY id LIMIT 1),
		'patient_status_ingest_column_mapping',
		'njb@integrichain.com'),
		('number_columns',
		(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'alkermes_vivitrol_patient_status_asembia')) AND id IN (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'number_columns' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = 'patient_status_standardize_numbers')))ORDER BY id LIMIT 1),
		'pharmacy_npi,pharmacy_ncpdp,pharmacy_zip,transaction_id,transaction_sequence,longitudinal_patient_id,patient_zip,hcp_zip,hcp_phone,hcp_npi,rx_fills,rx_fill_number,rx_refills_remaining,prev_dispensed,ndc,days_supply,ship_zip,primary_payer_bin,primary_payer_iin,primary_payer_pcn,secondary_payer_bin,secondary_payer_iin,secondary_payer_pcn,aggregator_ship_id,referral_number,primary_plan_paid,secondary_plan_paid,primary_copay,primary_coins,primary_deductible,primary_patient_responsibility,secondary_copay,secondary_coins,secondary_deductible,secondary_patient_responsibility,copay_as_amount,other_payer_amount,primary_cost_amount',
		'njb@integrichain.com');
COMMIT;
