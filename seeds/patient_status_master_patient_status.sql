BEGIN;
INSERT INTO transformation_templates (name, variable_structures, pipeline_state_type_id, last_actor) 
    VALUES       
        ('master_patient_status', 
        '{
            "input_transform":{"datatype": "string", "description": "The name of the transform to input source data from"},
            "col_status":{"datatype": "string","description": "The column of interest for this transform"}
        }', 
        (SELECT id FROM pipeline_state_types WHERE name = 'master'),
        'jshea@integrichain.com');
COMMIT;

BEGIN;
    INSERT INTO transformations
        (transformation_template_id, pipeline_state_id, graph_order, last_actor)
    VALUES
        ((SELECT id
            FROM transformation_templates
            WHERE name = 'master_patient_status'), (SELECT id
            FROM pipeline_states
            WHERE pipeline_state_type_id = (SELECT id
                FROM pipeline_state_types
                WHERE name = 'master') AND pipeline_id = (SELECT id
                FROM pipelines
                WHERE name = 'sun_all_brands_patient_status')), 0, 'jshea@integrichain.com'),
        ((SELECT id
            FROM transformation_templates
            WHERE name = 'master_patient_status'), (SELECT id
            FROM pipeline_states
            WHERE pipeline_state_type_id = (SELECT id
                FROM pipeline_state_types
                WHERE name = 'master') AND pipeline_id = (SELECT id
                FROM pipelines
                WHERE name = 'alkermes_vivitrol_patient_status')), 0, 'jshea@integrichain.com')                
                ;

    COMMIT;


BEGIN;
    ------------------------------------------------
    -- sun pipeline = sun_all_brands_patient_status
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
                WHERE name = 'sun_all_brands_patient_status')) 
                AND id IN (SELECT id
                FROM transformations
                WHERE (id NOT IN (SELECT t.id
                    FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id
                    WHERE tv.name = 'input_transform'
                    ORDER BY t.id)) AND id IN (SELECT t.id
                    from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id
                    WHERE tt.name = 'master_patient_status')))
            ORDER BY id LIMIT 1),
            'patient_status_ingest_brand_derivation', 
            'jshea@integrichain.com'),
    ('col_status',(SELECT id
    FROM transformations WHERE
    (pipeline_state_id IN
    (SELECT id
    FROM pipeline_states
    WHERE pipeline_id = (SELECT id
    FROM pipelines
    WHERE name = 'sun_all_brands_patient_status'))
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
        'customer_status',
        'jshea@integrichain.com');

    -----------------------------------------------------
    -- alkermes pipeline alkermes_vivitrol_patient_status
    -----------------------------------------------------   
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
                    WHERE tt.name = 'master_patient_status')))
            ORDER BY id LIMIT 1),
            'patient_status_standardize_dates', 
            'jshea@integrichain.com'),
    ('col_status',(SELECT id
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
        WHERE tv.name = 'col_status'
        ORDER BY t.id)) AND id IN (SELECT t.id
        from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id
        WHERE tt.name = 'master_patient_status')))
        ORDER BY id LIMIT 1), 
        'customer_status',
        'jshea@integrichain.com');   
    COMMIT;