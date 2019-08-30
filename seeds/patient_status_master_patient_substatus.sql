BEGIN;    
    INSERT INTO transformations
        (transformation_template_id, pipeline_state_id, graph_order, last_actor)
    VALUES
        ((SELECT id
            FROM transformation_templates
            WHERE name = 'master_patient_substatus'), (SELECT id
            FROM pipeline_states
            WHERE pipeline_state_type_id = (SELECT id
                FROM pipeline_state_types
                WHERE name = 'master') AND pipeline_id = (SELECT id
                FROM pipelines
                WHERE name = 'sun_allbrands_patient_status')), 1, 'jshea@integrichain.com'),
        ((SELECT id
            FROM transformation_templates
            WHERE name = 'master_patient_substatus'), (SELECT id
            FROM pipeline_states
            WHERE pipeline_state_type_id = (SELECT id
                FROM pipeline_state_types
                WHERE name = 'master') AND pipeline_id = (SELECT id
                FROM pipelines
                WHERE name = 'sun_odomzo_patient_status')), 1, 'jshea@integrichain.com'),
        ((SELECT id
            FROM transformation_templates
            WHERE name = 'master_patient_substatus'), (SELECT id
            FROM pipeline_states
            WHERE pipeline_state_type_id = (SELECT id
                FROM pipeline_state_types
                WHERE name = 'master') AND pipeline_id = (SELECT id
                FROM pipelines
                WHERE name = 'sun_yonsa_patient_status')), 1, 'jshea@integrichain.com');

    COMMIT;