BEGIN; 

    INSERT INTO transformations
        (transformation_template_id, pipeline_state_id, graph_order, last_actor)
    VALUES
        ((SELECT id
            FROM transformation_templates
            WHERE name = 'patient_status_fill_rate'), (SELECT id
            FROM pipeline_states
            WHERE pipeline_state_type_id = (SELECT id
                FROM pipeline_state_types
                WHERE name = 'metrics') AND pipeline_id = (SELECT id
                FROM pipelines
                WHERE name = 'sun_ilumya_patient_status')), 0, 'jlewis@integrichain.com'),
        ((SELECT id
            FROM transformation_templates
            WHERE name = 'patient_status_fill_rate'), (SELECT id
            FROM pipeline_states
            WHERE pipeline_state_type_id = (SELECT id
                FROM pipeline_state_types
                WHERE name = 'metrics') AND pipeline_id = (SELECT id
                FROM pipelines
                WHERE name = 'sun_odomzo_patient_status')), 0, 'jlewis@integrichain.com'),
        ((SELECT id
            FROM transformation_templates
            WHERE name = 'patient_status_fill_rate'), (SELECT id
            FROM pipeline_states
            WHERE pipeline_state_type_id = (SELECT id
                FROM pipeline_state_types
                WHERE name = 'metrics') AND pipeline_id = (SELECT id
                FROM pipelines
                WHERE name = 'bi_ofev_patient_status')), 0, 'jlewis@integrichain.com'),
        ((SELECT id
            FROM transformation_templates
            WHERE name = 'patient_status_fill_rate'), (SELECT id
            FROM pipeline_states
            WHERE pipeline_state_type_id = (SELECT id
                FROM pipeline_state_types
                WHERE name = 'metrics') AND pipeline_id = (SELECT id
                FROM pipelines
                WHERE name = 'alkermes_vivitrol_patient_status')), 0, 'jlewis@integrichain.com');

    COMMIT;

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
                WHERE name = 'sun_ilumya_patient_status')) AND id IN (SELECT id
                FROM transformations
                WHERE (id NOT IN (SELECT t.id
                    FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id
                    WHERE tv.name = 'input_transform'
                    ORDER BY t.id)) AND id IN (SELECT t.id
                    from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id
                    WHERE tt.name = 'patient_status_fill_rate')))
            ORDER BY id LIMIT 1), 'CHANGE THIS WHEN WE FIGURE OUT WHAT THE INPUT TRANSFORM IS', 'jlewis@integrichain.com'),
        ('shipment_status', (SELECT id
            FROM transformations
            WHERE (pipeline_state_id IN (SELECT id
                FROM pipeline_states
                WHERE pipeline_id = (SELECT id
                FROM pipelines
                WHERE name = 'sun_ilumya_patient_status')) AND id IN (SELECT id
                FROM transformations
                WHERE (id NOT IN (SELECT t.id
                    FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id
                    WHERE tv.name = 'shipment_status'
                    ORDER BY t.id)) AND id IN (SELECT t.id
                    from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id
                    WHERE tt.name = 'patient_status_fill_rate')))
            ORDER BY id LIMIT 1), 'SHIPMENT', 'jlewis@integrichain.com'),
        ('transfered_status', (SELECT id
            FROM transformations
            WHERE (pipeline_state_id IN (SELECT id
                FROM pipeline_states
                WHERE pipeline_id = (SELECT id
                FROM pipelines
                WHERE name = 'sun_ilumya_patient_status')) AND id IN (SELECT id
                FROM transformations
                WHERE (id NOT IN (SELECT t.id
                    FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id
                    WHERE tv.name = 'transfered_status'
                    ORDER BY t.id)) AND id IN (SELECT t.id
                    from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id
                    WHERE tt.name = 'patient_status_fill_rate')))
            ORDER BY id LIMIT 1), 'TRANSFERED', 'jlewis@integrichain.com'),
        ('cancelled_status', (SELECT id
            FROM transformations
            WHERE (pipeline_state_id IN (SELECT id
                FROM pipeline_states
                WHERE pipeline_id = (SELECT id
                FROM pipelines
                WHERE name = 'sun_ilumya_patient_status')) AND id IN (SELECT id
                FROM transformations
                WHERE (id NOT IN (SELECT t.id
                    FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id
                    WHERE tv.name = 'cancelled_status'
                    ORDER BY t.id)) AND id IN (SELECT t.id
                    from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id
                    WHERE tt.name = 'patient_status_fill_rate')))
            ORDER BY id LIMIT 1), 'CANCELLED', 'jlewis@integrichain.com'),
        ('open_status', (SELECT id
            FROM transformations
            WHERE (pipeline_state_id IN (SELECT id
                FROM pipeline_states
                WHERE pipeline_id = (SELECT id
                FROM pipelines
                WHERE name = 'sun_ilumya_patient_status')) AND id IN (SELECT id
                FROM transformations
                WHERE (id NOT IN (SELECT t.id
                    FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id
                    WHERE tv.name = 'open_status'
                    ORDER BY t.id)) AND id IN (SELECT t.id
                    from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id
                    WHERE tt.name = 'patient_status_fill_rate')))
            ORDER BY id LIMIT 1), 'OPEN', 'jlewis@integrichain.com'),
        ('filled_status', (SELECT id
            FROM transformations
            WHERE (pipeline_state_id IN (SELECT id
                FROM pipeline_states
                WHERE pipeline_id = (SELECT id
                FROM pipelines
                WHERE name = 'sun_ilumya_patient_status')) AND id IN (SELECT id
                FROM transformations
                WHERE (id NOT IN (SELECT t.id
                    FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id
                    WHERE tv.name = 'filled_status'
                    ORDER BY t.id)) AND id IN (SELECT t.id
                    from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id
                    WHERE tt.name = 'patient_status_fill_rate')))
            ORDER BY id LIMIT 1), 'FILLED', 'jlewis@integrichain.com')


    COMMIT;

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
                WHERE name = 'sun_ilumya_patient_status')) AND id IN (SELECT id
                FROM transformations
                WHERE (id NOT IN (SELECT t.id
                    FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id
                    WHERE tv.name = 'input_transform'
                    ORDER BY t.id)) AND id IN (SELECT t.id
                    from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id
                    WHERE tt.name = 'patient_status_fill_rate')))
            ORDER BY id LIMIT 1), 'CHANGE THIS WHEN WE FIGURE OUT WHAT THE INPUT TRANSFORM IS', 'jlewis@integrichain.com'),
        ('shipment_status', (SELECT id
            FROM transformations
            WHERE (pipeline_state_id IN (SELECT id
                FROM pipeline_states
                WHERE pipeline_id = (SELECT id
                FROM pipelines
                WHERE name = 'sun_odomzo_patient_status')) AND id IN (SELECT id
                FROM transformations
                WHERE (id NOT IN (SELECT t.id
                    FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id
                    WHERE tv.name = 'shipment_status'
                    ORDER BY t.id)) AND id IN (SELECT t.id
                    from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id
                    WHERE tt.name = 'patient_status_fill_rate')))
            ORDER BY id LIMIT 1), 'SHIPMENT', 'jlewis@integrichain.com'),
        ('transfered_status', (SELECT id
            FROM transformations
            WHERE (pipeline_state_id IN (SELECT id
                FROM pipeline_states
                WHERE pipeline_id = (SELECT id
                FROM pipelines
                WHERE name = 'sun_odomzo_patient_status')) AND id IN (SELECT id
                FROM transformations
                WHERE (id NOT IN (SELECT t.id
                    FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id
                    WHERE tv.name = 'transfered_status'
                    ORDER BY t.id)) AND id IN (SELECT t.id
                    from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id
                    WHERE tt.name = 'patient_status_fill_rate')))
            ORDER BY id LIMIT 1), 'TRANSFERED', 'jlewis@integrichain.com'),
        ('cancelled_status', (SELECT id
            FROM transformations
            WHERE (pipeline_state_id IN (SELECT id
                FROM pipeline_states
                WHERE pipeline_id = (SELECT id
                FROM pipelines
                WHERE name = 'sun_odomzo_patient_status')) AND id IN (SELECT id
                FROM transformations
                WHERE (id NOT IN (SELECT t.id
                    FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id
                    WHERE tv.name = 'cancelled_status'
                    ORDER BY t.id)) AND id IN (SELECT t.id
                    from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id
                    WHERE tt.name = 'patient_status_fill_rate')))
            ORDER BY id LIMIT 1), 'CANCELLED', 'jlewis@integrichain.com'),
        ('open_status', (SELECT id
            FROM transformations
            WHERE (pipeline_state_id IN (SELECT id
                FROM pipeline_states
                WHERE pipeline_id = (SELECT id
                FROM pipelines
                WHERE name = 'sun_odomzo_patient_status')) AND id IN (SELECT id
                FROM transformations
                WHERE (id NOT IN (SELECT t.id
                    FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id
                    WHERE tv.name = 'open_status'
                    ORDER BY t.id)) AND id IN (SELECT t.id
                    from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id
                    WHERE tt.name = 'patient_status_fill_rate')))
            ORDER BY id LIMIT 1), 'OPEN', 'jlewis@integrichain.com'),
        ('filled_status', (SELECT id
            FROM transformations
            WHERE (pipeline_state_id IN (SELECT id
                FROM pipeline_states
                WHERE pipeline_id = (SELECT id
                FROM pipelines
                WHERE name = 'sun_odomzo_patient_status')) AND id IN (SELECT id
                FROM transformations
                WHERE (id NOT IN (SELECT t.id
                    FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id
                    WHERE tv.name = 'filled_status'
                    ORDER BY t.id)) AND id IN (SELECT t.id
                    from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id
                    WHERE tt.name = 'patient_status_fill_rate')))
            ORDER BY id LIMIT 1), 'FILLED', 'jlewis@integrichain.com')


    COMMIT;

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
                WHERE name = 'sun_ilumya_patient_status')) AND id IN (SELECT id
                FROM transformations
                WHERE (id NOT IN (SELECT t.id
                    FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id
                    WHERE tv.name = 'input_transform'
                    ORDER BY t.id)) AND id IN (SELECT t.id
                    from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id
                    WHERE tt.name = 'patient_status_fill_rate')))
            ORDER BY id LIMIT 1), 'CHANGE THIS WHEN WE FIGURE OUT WHAT THE INPUT TRANSFORM IS', 'jlewis@integrichain.com'),
        ('shipment_status', (SELECT id
            FROM transformations
            WHERE (pipeline_state_id IN (SELECT id
                FROM pipeline_states
                WHERE pipeline_id = (SELECT id
                FROM pipelines
                WHERE name = 'bi_ofev_patient_status')) AND id IN (SELECT id
                FROM transformations
                WHERE (id NOT IN (SELECT t.id
                    FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id
                    WHERE tv.name = 'shipment_status'
                    ORDER BY t.id)) AND id IN (SELECT t.id
                    from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id
                    WHERE tt.name = 'patient_status_fill_rate')))
            ORDER BY id LIMIT 1), 'SHIPMENT', 'jlewis@integrichain.com'),
        ('transfered_status', (SELECT id
            FROM transformations
            WHERE (pipeline_state_id IN (SELECT id
                FROM pipeline_states
                WHERE pipeline_id = (SELECT id
                FROM pipelines
                WHERE name = 'bi_ofev_patient_status')) AND id IN (SELECT id
                FROM transformations
                WHERE (id NOT IN (SELECT t.id
                    FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id
                    WHERE tv.name = 'transfered_status'
                    ORDER BY t.id)) AND id IN (SELECT t.id
                    from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id
                    WHERE tt.name = 'patient_status_fill_rate')))
            ORDER BY id LIMIT 1), 'TRANSFERED', 'jlewis@integrichain.com'),
        ('cancelled_status', (SELECT id
            FROM transformations
            WHERE (pipeline_state_id IN (SELECT id
                FROM pipeline_states
                WHERE pipeline_id = (SELECT id
                FROM pipelines
                WHERE name = 'bi_ofev_patient_status')) AND id IN (SELECT id
                FROM transformations
                WHERE (id NOT IN (SELECT t.id
                    FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id
                    WHERE tv.name = 'cancelled_status'
                    ORDER BY t.id)) AND id IN (SELECT t.id
                    from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id
                    WHERE tt.name = 'patient_status_fill_rate')))
            ORDER BY id LIMIT 1), 'CANCELLED', 'jlewis@integrichain.com'),
        ('open_status', (SELECT id
            FROM transformations
            WHERE (pipeline_state_id IN (SELECT id
                FROM pipeline_states
                WHERE pipeline_id = (SELECT id
                FROM pipelines
                WHERE name = 'bi_ofev_patient_status')) AND id IN (SELECT id
                FROM transformations
                WHERE (id NOT IN (SELECT t.id
                    FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id
                    WHERE tv.name = 'open_status'
                    ORDER BY t.id)) AND id IN (SELECT t.id
                    from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id
                    WHERE tt.name = 'patient_status_fill_rate')))
            ORDER BY id LIMIT 1), 'OPEN', 'jlewis@integrichain.com'),
        ('filled_status', (SELECT id
            FROM transformations
            WHERE (pipeline_state_id IN (SELECT id
                FROM pipeline_states
                WHERE pipeline_id = (SELECT id
                FROM pipelines
                WHERE name = 'bi_ofev_patient_status')) AND id IN (SELECT id
                FROM transformations
                WHERE (id NOT IN (SELECT t.id
                    FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id
                    WHERE tv.name = 'filled_status'
                    ORDER BY t.id)) AND id IN (SELECT t.id
                    from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id
                    WHERE tt.name = 'patient_status_fill_rate')))
            ORDER BY id LIMIT 1), 'FILLED', 'jlewis@integrichain.com')


    COMMIT;

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
                WHERE name = 'sun_ilumya_patient_status')) AND id IN (SELECT id
                FROM transformations
                WHERE (id NOT IN (SELECT t.id
                    FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id
                    WHERE tv.name = 'input_transform'
                    ORDER BY t.id)) AND id IN (SELECT t.id
                    from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id
                    WHERE tt.name = 'patient_status_fill_rate')))
            ORDER BY id LIMIT 1), 'CHANGE THIS WHEN WE FIGURE OUT WHAT THE INPUT TRANSFORM IS', 'jlewis@integrichain.com'),
        ('shipment_status', (SELECT id
            FROM transformations
            WHERE (pipeline_state_id IN (SELECT id
                FROM pipeline_states
                WHERE pipeline_id = (SELECT id
                FROM pipelines
                WHERE name = 'alkermes_vivitrol_patient_status')) AND id IN (SELECT id
                FROM transformations
                WHERE (id NOT IN (SELECT t.id
                    FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id
                    WHERE tv.name = 'shipment_status'
                    ORDER BY t.id)) AND id IN (SELECT t.id
                    from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id
                    WHERE tt.name = 'patient_status_fill_rate')))
            ORDER BY id LIMIT 1), 'SHIPMENT', 'jlewis@integrichain.com'),
        ('transfered_status', (SELECT id
            FROM transformations
            WHERE (pipeline_state_id IN (SELECT id
                FROM pipeline_states
                WHERE pipeline_id = (SELECT id
                FROM pipelines
                WHERE name = 'alkermes_vivitrol_patient_status')) AND id IN (SELECT id
                FROM transformations
                WHERE (id NOT IN (SELECT t.id
                    FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id
                    WHERE tv.name = 'transfered_status'
                    ORDER BY t.id)) AND id IN (SELECT t.id
                    from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id
                    WHERE tt.name = 'patient_status_fill_rate')))
            ORDER BY id LIMIT 1), 'TRANSFERED', 'jlewis@integrichain.com'),
        ('cancelled_status', (SELECT id
            FROM transformations
            WHERE (pipeline_state_id IN (SELECT id
                FROM pipeline_states
                WHERE pipeline_id = (SELECT id
                FROM pipelines
                WHERE name = 'alkermes_vivitrol_patient_status')) AND id IN (SELECT id
                FROM transformations
                WHERE (id NOT IN (SELECT t.id
                    FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id
                    WHERE tv.name = 'cancelled_status'
                    ORDER BY t.id)) AND id IN (SELECT t.id
                    from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id
                    WHERE tt.name = 'patient_status_fill_rate')))
            ORDER BY id LIMIT 1), 'CANCELLED', 'jlewis@integrichain.com'),
        ('open_status', (SELECT id
            FROM transformations
            WHERE (pipeline_state_id IN (SELECT id
                FROM pipeline_states
                WHERE pipeline_id = (SELECT id
                FROM pipelines
                WHERE name = 'alkermes_vivitrol_patient_status')) AND id IN (SELECT id
                FROM transformations
                WHERE (id NOT IN (SELECT t.id
                    FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id
                    WHERE tv.name = 'open_status'
                    ORDER BY t.id)) AND id IN (SELECT t.id
                    from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id
                    WHERE tt.name = 'patient_status_fill_rate')))
            ORDER BY id LIMIT 1), 'OPEN', 'jlewis@integrichain.com'),
        ('filled_status', (SELECT id
            FROM transformations
            WHERE (pipeline_state_id IN (SELECT id
                FROM pipeline_states
                WHERE pipeline_id = (SELECT id
                FROM pipelines
                WHERE name = 'alkermes_vivitrol_patient_status')) AND id IN (SELECT id
                FROM transformations
                WHERE (id NOT IN (SELECT t.id
                    FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id
                    WHERE tv.name = 'filled_status'
                    ORDER BY t.id)) AND id IN (SELECT t.id
                    from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id
                    WHERE tt.name = 'patient_status_fill_rate')))
            ORDER BY id LIMIT 1), 'FILLED', 'jlewis@integrichain.com')


    COMMIT;

    