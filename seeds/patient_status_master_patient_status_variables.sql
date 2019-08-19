
BEGIN;

    INSERT INTO transformation_variables
        (name, transformation_id, value, last_actor)
    VALUES
        ('input_transform', (SELECT id
            FROM transformations
            WHERE (pipeline_state_id IN (SELECT id
                FROM pipeline_states
                WHERE pipeline_id = (SELECT id
                FROM pipelines
                WHERE name = 'sun_ilumya_patient_status')) 
                AND id IN (SELECT id
                FROM transformations
                WHERE (id NOT IN (SELECT t.id
                    FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id
                    WHERE tv.name = 'input_transform'
                    ORDER BY t.id)) AND id IN (SELECT t.id
                    from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id
                    WHERE tt.name = 'master_patient_status')))
            ORDER BY id LIMIT 1),
            'sun_ilumya_patient_status', 
            'jshea@integrichain.com'),
    ('col_status',(SELECT id
    FROM transformations WHERE
    (pipeline_state_id IN
    (SELECT id
    FROM pipeline_states
    WHERE pipeline_id = (SELECT id
    FROM pipelines
    WHERE name = 'sun_ilumya_patient_status'))
    AND id IN
    (SELECT id
    FROM transformations
    WHERE (id NOT IN (SELECT t.id
        FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id
        WHERE tv.name = 'col_status'
        ORDER BY t.id)) AND id IN (SELECT t.id
        from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id
        WHERE tt.name = 'master_patient_status')))
        ORDER BY id LIMIT 1), 
        'status_code',
        'jshea@integrichain.com');


       -- next sun pipeline
       
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
                    WHERE tt.name = 'master_patient_status')))
            ORDER BY id LIMIT 1),
            'sun_odomzo_patient_status', 
            'jshea@integrichain.com'),
    ('col_status',(SELECT id
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
        WHERE tv.name = 'col_status'
        ORDER BY t.id)) AND id IN (SELECT t.id
        from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id
        WHERE tt.name = 'master_patient_status')))
        ORDER BY id LIMIT 1), 
        'status_code',
        'jshea@integrichain.com');
    
    -- next sun pipeline
       
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
                    WHERE tt.name = 'master_patient_status')))
            ORDER BY id LIMIT 1),
            'sun_yonsa_patient_status', 
            'jshea@integrichain.com'),
    ('col_status',(SELECT id
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
        WHERE tv.name = 'col_status'
        ORDER BY t.id)) AND id IN (SELECT t.id
        from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id
        WHERE tt.name = 'master_patient_status')))
        ORDER BY id LIMIT 1), 
        'status_code',
        'jshea@integrichain.com');   
       
    COMMIT;

   
