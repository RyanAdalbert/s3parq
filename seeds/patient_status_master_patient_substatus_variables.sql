
BEGIN;
    ------------------------------------------------
    -- sun pipeline = sun_ilumya_patient_status
    -------------------------------------------
    INSERT INTO transformation_variables
        (name, transformation_id, value, last_actor)
    VALUES
        ('input_transform', (SELECT id
            FROM transformations
            WHERE (pipeline_state_id IN (SELECT id
                FROM pipeline_states
                WHERE pipeline_id = (SELECT id
                FROM pipelines
                WHERE name = 'sun_allbrands_patient_status')) 
                AND id IN (SELECT id
                FROM transformations
                WHERE (id NOT IN (SELECT t.id
                    FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id
                    WHERE tv.name = 'input_transform'
                    ORDER BY t.id)) AND id IN (SELECT t.id
                    from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id
                    WHERE tt.name = 'master_patient_substatus')))
            ORDER BY id LIMIT 1),
            'master_patient_status', 
            'jshea@integrichain.com'),
    ('col_substatus',(SELECT id
    FROM transformations WHERE
    (pipeline_state_id IN
    (SELECT id
    FROM pipeline_states
    WHERE pipeline_id = (SELECT id
    FROM pipelines
    WHERE name = 'sun_allbrands_patient_status'))
    AND id IN
    (SELECT id
    FROM transformations
    WHERE (id NOT IN (SELECT t.id
        FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id
        WHERE tv.name = 'col_substatus'
        ORDER BY t.id)) AND id IN (SELECT t.id
        from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id
        WHERE tt.name = 'master_patient_substatus')))
        ORDER BY id LIMIT 1), 
        'customer_substatus',
        'jshea@integrichain.com')
		,
		    ('col_customer_name',(SELECT id
		    FROM transformations WHERE
		    (pipeline_state_id IN
		    (SELECT id
		    FROM pipeline_states
		    WHERE pipeline_id = (SELECT id
		    FROM pipelines
		    WHERE name = 'sun_allbrands_patient_status'))
		    AND id IN
		    (SELECT id
		    FROM transformations
		    WHERE (id NOT IN (SELECT t.id
		        FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id
		        WHERE tv.name = 'col_customer_name'
		        ORDER BY t.id)) AND id IN (SELECT t.id
		        from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id
		        WHERE tt.name = 'master_patient_substatus')))
		        ORDER BY id LIMIT 1), 
		        'sun',
		        'jshea@integrichain.com')
		;

    ------------------------------------------------
    -- next sun pipeline = sun_odomzo_patient_status
    ------------------------------------------------   
    INSERT INTO transformation_variables
        (name, transformation_id, value, last_actor)
    VALUES
        ('input_transform', (SELECT id
            FROM transformations
            WHERE (pipeline_state_id IN (SELECT id
                FROM pipeline_states
                WHERE pipeline_id = (SELECT id
                FROM pipelines
                WHERE name = 'sun_odomzo_patient_status')) 
                AND id IN (SELECT id
                FROM transformations
                WHERE (id NOT IN (SELECT t.id
                    FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id
                    WHERE tv.name = 'input_transform'
                    ORDER BY t.id)) AND id IN (SELECT t.id
                    from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id
                    WHERE tt.name = 'master_patient_substatus')))
            ORDER BY id LIMIT 1),
            'master_patient_status', 
            'jshea@integrichain.com'),
    ('col_substatus',(SELECT id
    FROM transformations WHERE
    (pipeline_state_id IN
    (SELECT id
    FROM pipeline_states
    WHERE pipeline_id = (SELECT id
    FROM pipelines
    WHERE name = 'sun_odomzo_patient_status'))
    AND id IN
    (SELECT id
    FROM transformations
    WHERE (id NOT IN (SELECT t.id
        FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id
        WHERE tv.name = 'col_substatus'
        ORDER BY t.id)) AND id IN (SELECT t.id
        from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id
        WHERE tt.name = 'master_patient_substatus')))
        ORDER BY id LIMIT 1), 
        'customer_substatus',
        'jshea@integrichain.com')
		,
		    ('col_customer_name',(SELECT id
		    FROM transformations WHERE
		    (pipeline_state_id IN
		    (SELECT id
		    FROM pipeline_states
		    WHERE pipeline_id = (SELECT id
		    FROM pipelines
		    WHERE name = 'sun_odomzo_patient_status'))
		    AND id IN
		    (SELECT id
		    FROM transformations
		    WHERE (id NOT IN (SELECT t.id
		        FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id
		        WHERE tv.name = 'col_substatus'
		        ORDER BY t.id)) AND id IN (SELECT t.id
		        from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id
		        WHERE tt.name = 'master_patient_substatus')))
		        ORDER BY id LIMIT 1), 
		        'sun',
		        'jshea@integrichain.com');
    ------------------------------------------------
    -- next sun pipeline = sun_yonsa_patient_status
    -----------------------------------------------   
    INSERT INTO transformation_variables
        (name, transformation_id, value, last_actor)
    VALUES
        ('input_transform', (SELECT id
            FROM transformations
            WHERE (pipeline_state_id IN (SELECT id
                FROM pipeline_states
                WHERE pipeline_id = (SELECT id
                FROM pipelines
                WHERE name = 'sun_yonsa_patient_status')) 
                AND id IN (SELECT id
                FROM transformations
                WHERE (id NOT IN (SELECT t.id
                    FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id
                    WHERE tv.name = 'input_transform'
                    ORDER BY t.id)) AND id IN (SELECT t.id
                    from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id
                    WHERE tt.name = 'master_patient_substatus')))
            ORDER BY id LIMIT 1),
            'master_patient_status', 
            'jshea@integrichain.com'),
    ('col_substatus',(SELECT id
    FROM transformations WHERE
    (pipeline_state_id IN
    (SELECT id
    FROM pipeline_states
    WHERE pipeline_id = (SELECT id
    FROM pipelines
    WHERE name = 'sun_yonsa_patient_status'))
    AND id IN
    (SELECT id
    FROM transformations
    WHERE (id NOT IN (SELECT t.id
        FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id
        WHERE tv.name = 'col_substatus'
        ORDER BY t.id)) AND id IN (SELECT t.id
        from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id
        WHERE tt.name = 'master_patient_substatus')))
        ORDER BY id LIMIT 1), 
        'customer_substatus',
        'jshea@integrichain.com')
		,
		    ('col_customer_name',(SELECT id
		    FROM transformations WHERE
		    (pipeline_state_id IN
		    (SELECT id
		    FROM pipeline_states
		    WHERE pipeline_id = (SELECT id
		    FROM pipelines
		    WHERE name = 'sun_yonsa_patient_status'))
		    AND id IN
		    (SELECT id
		    FROM transformations
		    WHERE (id NOT IN (SELECT t.id
		        FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id
		        WHERE tv.name = 'col_substatus'
		        ORDER BY t.id)) AND id IN (SELECT t.id
		        from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id
		        WHERE tt.name = 'master_patient_substatus')))
		        ORDER BY id LIMIT 1), 
		        'sun',
		        'jshea@integrichain.com');   
    -----------------------------------------------------
    -- alkermes pipeline alkermes_vivitrol_patient_status
    ------------------------------------------------------
    INSERT INTO transformation_variables
        (name, transformation_id, value, last_actor)
    VALUES
        ('input_transform', (SELECT id
            FROM transformations
            WHERE (pipeline_state_id IN (SELECT id
                FROM pipeline_states
                WHERE pipeline_id = (SELECT id
                FROM pipelines
                WHERE name = 'alkermes_vivitrol_patient_status')) 
                AND id IN (SELECT id
                FROM transformations
                WHERE (id NOT IN (SELECT t.id
                    FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id
                    WHERE tv.name = 'input_transform'
                    ORDER BY t.id)) AND id IN (SELECT t.id
                    from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id
                    WHERE tt.name = 'master_patient_substatus')))
            ORDER BY id LIMIT 1),
            'master_patient_status', 
            'jshea@integrichain.com'),
    ('col_substatus',(SELECT id
    FROM transformations WHERE
    (pipeline_state_id IN
    (SELECT id
    FROM pipeline_states
    WHERE pipeline_id = (SELECT id
    FROM pipelines
    WHERE name = 'alkermes_vivitrol_patient_status'))
    AND id IN
    (SELECT id
    FROM transformations
    WHERE (id NOT IN (SELECT t.id
        FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id
        WHERE tv.name = 'col_substatus'
        ORDER BY t.id)) AND id IN (SELECT t.id
        from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id
        WHERE tt.name = 'master_patient_substatus')))
        ORDER BY id LIMIT 1), 
        'customer_status_description',
        'jshea@integrichain.com')
		,
		    ('col_customer_name',(SELECT id
		    FROM transformations WHERE
		    (pipeline_state_id IN
		    (SELECT id
		    FROM pipeline_states
		    WHERE pipeline_id = (SELECT id
		    FROM pipelines
		    WHERE name = 'alkermes_vivitrol_patient_status'))
		    AND id IN
		    (SELECT id
		    FROM transformations
		    WHERE (id NOT IN (SELECT t.id
		        FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id
		        WHERE tv.name = 'col_substatus'
		        ORDER BY t.id)) AND id IN (SELECT t.id
		        from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id
		        WHERE tt.name = 'master_patient_substatus')))
		        ORDER BY id LIMIT 1), 
		        'alkermes',
		        'jshea@integrichain.com');  

       
    COMMIT;

   
