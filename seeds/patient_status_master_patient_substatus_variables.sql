
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
                WHERE name = 'sun_patient_journey')) 
                AND id IN (SELECT id
                FROM transformations
                WHERE (id NOT IN (SELECT t.id
                    FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id
                    WHERE tv.name = 'input_transform'
                    ORDER BY t.id)) AND id IN (SELECT t.id
                    from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id
                    WHERE tt.name = 'master_patient_substatus')))
            ORDER BY id LIMIT 1),
            'symphony_health_association_ingest_column_mapping', 
            'jshea@integrichain.com'),
    ('col_substatus',(SELECT id
    FROM transformations WHERE
    (pipeline_state_id IN
    (SELECT id
    FROM pipeline_states
    WHERE pipeline_id = (SELECT id
    FROM pipelines
    WHERE name = 'sun_patient_journey'))
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
        'sub_status',
        'jshea@integrichain.com')
		,
		    ('customer_name',(SELECT id
		    FROM transformations WHERE
		    (pipeline_state_id IN
		    (SELECT id
		    FROM pipeline_states
		    WHERE pipeline_id = (SELECT id
		    FROM pipelines
		    WHERE name = 'sun_patient_journey'))
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
		        'jshea@integrichain.com')
		;


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
                WHERE name = 'sun_ilumya_extract')) 
                AND id IN (SELECT id
                FROM transformations
                WHERE (id NOT IN (SELECT t.id
                    FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id
                    WHERE tv.name = 'input_transform'
                    ORDER BY t.id)) AND id IN (SELECT t.id
                    from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id
                    WHERE tt.name = 'master_patient_substatus')))
            ORDER BY id LIMIT 1),
            'symphony_health_association_ingest_column_mapping', 
            'jshea@integrichain.com'),
    ('col_substatus',(SELECT id
    FROM transformations WHERE
    (pipeline_state_id IN
    (SELECT id
    FROM pipeline_states
    WHERE pipeline_id = (SELECT id
    FROM pipelines
    WHERE name = 'sun_ilumya_extract'))
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
        'sub_status',
        'jshea@integrichain.com')
		,
		    ('customer_name',(SELECT id
		    FROM transformations WHERE
		    (pipeline_state_id IN
		    (SELECT id
		    FROM pipeline_states
		    WHERE pipeline_id = (SELECT id
		    FROM pipelines
		    WHERE name = 'sun_ilumya_extract'))
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
    
    -- next/final sun pipeline
       
    INSERT INTO transformation_variables
        (name, transformation_id, value, last_actor)
    VALUES
        ('input_transform', (SELECT id
            FROM transformations
            WHERE (pipeline_state_id IN (SELECT id
                FROM pipeline_states
                WHERE pipeline_id = (SELECT id
                FROM pipelines
                WHERE name = 'sun_odomzo_extract')) 
                AND id IN (SELECT id
                FROM transformations
                WHERE (id NOT IN (SELECT t.id
                    FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id
                    WHERE tv.name = 'input_transform'
                    ORDER BY t.id)) AND id IN (SELECT t.id
                    from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id
                    WHERE tt.name = 'master_patient_substatus')))
            ORDER BY id LIMIT 1),
            'symphony_health_association_ingest_column_mapping', 
            'jshea@integrichain.com'),
    ('col_substatus',(SELECT id
    FROM transformations WHERE
    (pipeline_state_id IN
    (SELECT id
    FROM pipeline_states
    WHERE pipeline_id = (SELECT id
    FROM pipelines
    WHERE name = 'sun_odomzo_extract'))
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
        'sub_status',
        'jshea@integrichain.com')
		,
		    ('customer_name',(SELECT id
		    FROM transformations WHERE
		    (pipeline_state_id IN
		    (SELECT id
		    FROM pipeline_states
		    WHERE pipeline_id = (SELECT id
		    FROM pipelines
		    WHERE name = 'sun_odomzo_extract'))
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
       
    COMMIT;

   
