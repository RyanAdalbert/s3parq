BEGIN;
    INSERT INTO transformations
        (transformation_template_id, pipeline_state_id, graph_order, last_actor)
    VALUES
        ((SELECT id
            FROM transformation_templates
            WHERE name = 'patient_status_enrich_patient_journey_hierarchy'), (SELECT id
            FROM pipeline_states
            WHERE pipeline_state_type_id = (SELECT id
                FROM pipeline_state_types
                WHERE name = 'enrich') AND pipeline_id = (SELECT id
                FROM pipelines
                WHERE name = 'sun_ilumya_patient_status')), 0, 'jshea@integrichain.com'),
        ((SELECT id
            FROM transformation_templates
            WHERE name = 'patient_status_enrich_patient_journey_hierarchy'), (SELECT id
            FROM pipeline_states
            WHERE pipeline_state_type_id = (SELECT id
                FROM pipeline_state_types
                WHERE name = 'enrich') AND pipeline_id = (SELECT id
                FROM pipelines
                WHERE name = 'sun_odomzo_patient_status')), 0, 'jshea@integrichain.com'),
        ((SELECT id
            FROM transformation_templates
            WHERE name = 'patient_status_enrich_patient_journey_hierarchy'), (SELECT id
            FROM pipeline_states
            WHERE pipeline_state_type_id = (SELECT id
                FROM pipeline_state_types
                WHERE name = 'enrich') AND pipeline_id = (SELECT id
                FROM pipelines
                WHERE name = 'sun_yonsa_patient_status')), 0, 'jshea@integrichain.com'),
        ((SELECT id
            FROM transformation_templates
            WHERE name = 'patient_status_enrich_patient_journey_hierarchy'), (SELECT id
            FROM pipeline_states
            WHERE pipeline_state_type_id = (SELECT id
                FROM pipeline_state_types
                WHERE name = 'enrich') AND pipeline_id = (SELECT id
                FROM pipelines
                WHERE name = 'alkermes_vivitrol_patient_status')), 0, 'jshea@integrichain.com')   
                ;

    COMMIT;