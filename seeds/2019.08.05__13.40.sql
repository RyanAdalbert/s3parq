BEGIN;


INSERT INTO pipelines (name, is_active, description, pipeline_type_id, brand_id, run_frequency, last_actor)
    VALUES
        ('sun_yonsa_patient_status', TRUE, 'Sun patient status pipeline -- YONSA', (SELECT id FROM pipeline_types WHERE name = 'patient_journey'), (SELECT id from brands WHERE name = 'ILUMYA'), 'weekly', 'jtobias@integrichain.com');

INSERT INTO pipeline_states (pipeline_state_type_id, pipeline_id, graph_order, last_actor)
    VALUES 
((SELECT id FROM pipeline_state_types WHERE name = 'raw'), (SELECT id FROM pipelines WHERE name = 'sun_yonsa_patient_status'), 0, 'jtobias@integrichain.com'),
((SELECT id FROM pipeline_state_types WHERE name = 'ingest'), (SELECT id FROM pipelines WHERE name = 'sun_yonsa_patient_status'), 1, 'jtobias@integrichain.com'),
((SELECT id FROM pipeline_state_types WHERE name = 'master'), (SELECT id FROM pipelines WHERE name = 'sun_yonsa_patient_status'), 3, 'jtobias@integrichain.com'),
((SELECT id FROM pipeline_state_types WHERE name = 'enhance'), (SELECT id FROM pipelines WHERE name = 'sun_yonsa_patient_status'), 4, 'jtobias@integrichain.com'),
((SELECT id FROM pipeline_state_types WHERE name = 'enrich'), (SELECT id FROM pipelines WHERE name = 'sun_yonsa_patient_status'), 5, 'jtobias@integrichain.com'),
((SELECT id FROM pipeline_state_types WHERE name = 'metrics'), (SELECT id FROM pipelines WHERE name = 'sun_yonsa_patient_status'), 6, 'jtobias@integrichain.com'),
((SELECT id FROM pipeline_state_types WHERE name = 'dimensional'), (SELECT id FROM pipelines WHERE name = 'sun_yonsa_patient_status'), 7, 'jtobias@integrichain.com'),
((SELECT id FROM pipeline_state_types WHERE name = 'master'), (SELECT id FROM pipelines WHERE name = 'sun_ilumya_patient_status'), 3, 'jtobias@integrichain.com'),
((SELECT id FROM pipeline_state_types WHERE name = 'enhance'), (SELECT id FROM pipelines WHERE name = 'sun_ilumya_patient_status'), 4, 'jtobias@integrichain.com'),
((SELECT id FROM pipeline_state_types WHERE name = 'enrich'), (SELECT id FROM pipelines WHERE name = 'sun_ilumya_patient_status'), 5, 'jtobias@integrichain.com'),
((SELECT id FROM pipeline_state_types WHERE name = 'metrics'), (SELECT id FROM pipelines WHERE name = 'sun_ilumya_patient_status'), 6, 'jtobias@integrichain.com'),
((SELECT id FROM pipeline_state_types WHERE name = 'dimensional'), (SELECT id FROM pipelines WHERE name = 'sun_ilumya_patient_status'), 7, 'jtobias@integrichain.com'),
((SELECT id FROM pipeline_state_types WHERE name = 'master'), (SELECT id FROM pipelines WHERE name = 'sun_odomzo_patient_status'), 3, 'jtobias@integrichain.com'),
((SELECT id FROM pipeline_state_types WHERE name = 'enhance'), (SELECT id FROM pipelines WHERE name = 'sun_odomzo_patient_status'), 4, 'jtobias@integrichain.com'),
((SELECT id FROM pipeline_state_types WHERE name = 'enrich'), (SELECT id FROM pipelines WHERE name = 'sun_odomzo_patient_status'), 5, 'jtobias@integrichain.com'),
((SELECT id FROM pipeline_state_types WHERE name = 'metrics'), (SELECT id FROM pipelines WHERE name = 'sun_odomzo_patient_status'), 6, 'jtobias@integrichain.com'),
((SELECT id FROM pipeline_state_types WHERE name = 'dimensional'), (SELECT id FROM pipelines WHERE name = 'sun_odomzo_patient_status'), 7, 'jtobias@integrichain.com'),
((SELECT id FROM pipeline_state_types WHERE name = 'master'), (SELECT id FROM pipelines WHERE name = 'bi_ofev_patient_status'), 3, 'jtobias@integrichain.com'),
((SELECT id FROM pipeline_state_types WHERE name = 'enhance'), (SELECT id FROM pipelines WHERE name = 'bi_ofev_patient_status'), 4, 'jtobias@integrichain.com'),
((SELECT id FROM pipeline_state_types WHERE name = 'enrich'), (SELECT id FROM pipelines WHERE name = 'bi_ofev_patient_status'), 5, 'jtobias@integrichain.com'),
((SELECT id FROM pipeline_state_types WHERE name = 'metrics'), (SELECT id FROM pipelines WHERE name = 'bi_ofev_patient_status'), 6, 'jtobias@integrichain.com'),
((SELECT id FROM pipeline_state_types WHERE name = 'dimensional'), (SELECT id FROM pipelines WHERE name = 'bi_ofev_patient_status'), 7, 'jtobias@integrichain.com'),
((SELECT id FROM pipeline_state_types WHERE name = 'master'), (SELECT id FROM pipelines WHERE name = 'alkermes_vivitrol_patient_status'), 3, 'jtobias@integrichain.com'),
((SELECT id FROM pipeline_state_types WHERE name = 'enhance'), (SELECT id FROM pipelines WHERE name = 'alkermes_vivitrol_patient_status'), 4, 'jtobias@integrichain.com'),
((SELECT id FROM pipeline_state_types WHERE name = 'enrich'), (SELECT id FROM pipelines WHERE name = 'alkermes_vivitrol_patient_status'), 5, 'jtobias@integrichain.com'),
((SELECT id FROM pipeline_state_types WHERE name = 'metrics'), (SELECT id FROM pipelines WHERE name = 'alkermes_vivitrol_patient_status'), 6, 'jtobias@integrichain.com'),
((SELECT id FROM pipeline_state_types WHERE name = 'dimensional'), (SELECT id FROM pipelines WHERE name = 'alkermes_vivitrol_patient_status'), 7, 'jtobias@integrichain.com');

COMMIT;
