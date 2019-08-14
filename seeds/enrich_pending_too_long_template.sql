BEGIN;
INSERT INTO transformation_templates (name, variable_structures, pipeline_state_type_id, last_actor) 
    VALUES
       ('enrich_pending_too_long', 
        '{"input_transform":{"datatype": "string", "description": "The name of the transform to input source data from"},   "unique_id":{"datatype": "string", "description": "ID for ic_{id}_ptl modification"}, "trans_id":{"datatype": "str", "description": "Transaction ID"},    "brand_col":{"datatype": "str", "description": "Brand"},    "patient_id":{"datatype": "str", "description": "Patient ID"},      "pharmacy":{"datatype": "str", "description": "Pharmacy"},      "status_date":{"datatype": "str", "description": "status date"},    "referral_date":{"datatype": "str", "description": "Referral Date"},    "status":{"datatype": "str", "description": "Status"},      "substatus":{"datatype": "str", "description": "Substatus"},    "hierarchy":{"datatype": "str", "description": "Hierarchy"},    "pending_status_code":{"datatype": "str", "description": "Pending status code (customer-specific)"},    "cancel_status_code":{"datatype": "str", "description": "Cancel status code (customer-specific)"},      "pending_too_long_code":{"datatype": "str", "description": "Pending Too Long status code"},     "ptl_threshold":{"datatype": "int", "description": "Number of days threshold for inserting a PENDING TOO LONG record (customer-specific)"}}',
        (SELECT id FROM pipeline_state_types WHERE name = 'enrich'),
        'jtobias@integrichain.com');
COMMIT;
