BEGIN;

    INSERT INTO pipelines (name, is_active, description, pipeline_type_id, brand_id, run_frequency, last_actor)
        VALUES
            ('sun_ilumya_patient_status', TRUE, 'Sun patient status pipeline -- ILUMYA', (SELECT id FROM pipeline_types WHERE name = 'patient_journey'), (SELECT id from brands WHERE name = 'ILUMYA'), 'weekly', 'rns@integrichain.com'),
            ('sun_odomzo_patient_status', TRUE, 'Sun patient status pipeline -- ODOMZO', (SELECT id FROM pipeline_types WHERE name = 'patient_journey'), (SELECT id from brands WHERE name = 'ODOMZO'), 'weekly', 'rns@integrichain.com'),
            ('sun_yonsa_patient_status', TRUE, 'Sun patient status pipeline -- YONSA', (SELECT id FROM pipeline_types WHERE name = 'patient_journey'), (SELECT id from brands WHERE name = 'ILUMYA'), 'weekly', 'jtobias@integrichain.com'),
            ('bi_ofev_patient_status', TRUE, 'BI patient status pipeline -- OFEV', (SELECT id FROM pipeline_types WHERE name = 'patient_journey'), (SELECT id from brands WHERE name = 'OFEV'), 'weekly', 'rns@integrichain.com'),
            ('alkermes_vivitrol_patient_status', TRUE, 'Alkermes patient status pipeline -- VIVITROL', (SELECT id FROM pipeline_types WHERE name = 'patient_journey'), (SELECT id from brands WHERE name = 'VIVITROL'), 'weekly', 'rns@integrichain.com'),
            ('sun_ilumya_extract', TRUE, 'Extract for Symphony Health Association -- ILUMYA', (SELECT id FROM pipeline_types WHERE name = 'patient_journey'), (SELECT id from brands WHERE name = 'ILUMYA'), 'weekly', 'njb@integrichain.com'),
            ('sun_odomzo_extract', TRUE, 'Extract for Symphony Health Association -- ODOMZO', (SELECT id FROM pipeline_types WHERE name = 'patient_journey'), (SELECT id from brands WHERE name = 'ODOMZO'), 'weekly', 'njb@integrichain.com');

INSERT INTO pipeline_states (pipeline_state_type_id, pipeline_id, graph_order, last_actor)
    VALUES 
        ((SELECT id FROM pipeline_state_types WHERE name = 'raw'), (SELECT id FROM pipelines WHERE name = 'sun_ilumya_patient_status'), 0, 'rns@integrichain.com'),
        ((SELECT id FROM pipeline_state_types WHERE name = 'ingest'), (SELECT id FROM pipelines WHERE name = 'sun_ilumya_patient_status'), 1, 'rns@integrichain.com'),
        ((SELECT id FROM pipeline_state_types WHERE name = 'master'), (SELECT id FROM pipelines WHERE name = 'sun_ilumya_patient_status'), 2, 'jtobias@integrichain.com'),
        ((SELECT id FROM pipeline_state_types WHERE name = 'enhance'), (SELECT id FROM pipelines WHERE name = 'sun_ilumya_patient_status'), 3, 'jtobias@integrichain.com'),
        ((SELECT id FROM pipeline_state_types WHERE name = 'enrich'), (SELECT id FROM pipelines WHERE name = 'sun_ilumya_patient_status'), 4, 'jtobias@integrichain.com'),
        ((SELECT id FROM pipeline_state_types WHERE name = 'metrics'), (SELECT id FROM pipelines WHERE name = 'sun_ilumya_patient_status'), 5, 'jtobias@integrichain.com'),
        ((SELECT id FROM pipeline_state_types WHERE name = 'dimensional'), (SELECT id FROM pipelines WHERE name = 'sun_ilumya_patient_status'), 6, 'jtobias@integrichain.com'),

        ((SELECT id FROM pipeline_state_types WHERE name = 'raw'), (SELECT id FROM pipelines WHERE name = 'sun_odomzo_patient_status'), 0, 'rns@integrichain.com'),
        ((SELECT id FROM pipeline_state_types WHERE name = 'ingest'), (SELECT id FROM pipelines WHERE name = 'sun_odomzo_patient_status'), 1, 'rns@integrichain.com'),
        ((SELECT id FROM pipeline_state_types WHERE name = 'master'), (SELECT id FROM pipelines WHERE name = 'sun_odomzo_patient_status'), 2, 'jtobias@integrichain.com'),
        ((SELECT id FROM pipeline_state_types WHERE name = 'enhance'), (SELECT id FROM pipelines WHERE name = 'sun_odomzo_patient_status'), 3, 'jtobias@integrichain.com'),
        ((SELECT id FROM pipeline_state_types WHERE name = 'enrich'), (SELECT id FROM pipelines WHERE name = 'sun_odomzo_patient_status'), 4, 'jtobias@integrichain.com'),
        ((SELECT id FROM pipeline_state_types WHERE name = 'metrics'), (SELECT id FROM pipelines WHERE name = 'sun_odomzo_patient_status'), 5, 'jtobias@integrichain.com'),
        ((SELECT id FROM pipeline_state_types WHERE name = 'dimensional'), (SELECT id FROM pipelines WHERE name = 'sun_odomzo_patient_status'), 6, 'jtobias@integrichain.com'),

        ((SELECT id FROM pipeline_state_types WHERE name = 'raw'), (SELECT id FROM pipelines WHERE name = 'sun_yonsa_patient_status'), 0, 'jtobias@integrichain.com'),
        ((SELECT id FROM pipeline_state_types WHERE name = 'ingest'), (SELECT id FROM pipelines WHERE name = 'sun_yonsa_patient_status'), 1, 'jtobias@integrichain.com'),
        ((SELECT id FROM pipeline_state_types WHERE name = 'master'), (SELECT id FROM pipelines WHERE name = 'sun_yonsa_patient_status'), 2, 'jtobias@integrichain.com'),
        ((SELECT id FROM pipeline_state_types WHERE name = 'enhance'), (SELECT id FROM pipelines WHERE name = 'sun_yonsa_patient_status'), 3, 'jtobias@integrichain.com'),
        ((SELECT id FROM pipeline_state_types WHERE name = 'enrich'), (SELECT id FROM pipelines WHERE name = 'sun_yonsa_patient_status'), 4, 'jtobias@integrichain.com'),
        ((SELECT id FROM pipeline_state_types WHERE name = 'metrics'), (SELECT id FROM pipelines WHERE name = 'sun_yonsa_patient_status'), 5, 'jtobias@integrichain.com'),
        ((SELECT id FROM pipeline_state_types WHERE name = 'dimensional'), (SELECT id FROM pipelines WHERE name = 'sun_yonsa_patient_status'), 6, 'jtobias@integrichain.com'),

        ((SELECT id FROM pipeline_state_types WHERE name = 'raw'), (SELECT id FROM pipelines WHERE name = 'sun_ilumya_extract'), 0, 'njb@integrichain.com'),
        ((SELECT id FROM pipeline_state_types WHERE name = 'ingest'), (SELECT id FROM pipelines WHERE name = 'sun_ilumya_extract'), 1, 'njb@integrichain.com'),
        ((SELECT id FROM pipeline_state_types WHERE name = 'master'), (SELECT id FROM pipelines WHERE name = 'sun_ilumya_extract'), 2, 'njb@integrichain.com'),
        ((SELECT id FROM pipeline_state_types WHERE name = 'enrich'), (SELECT id FROM pipelines WHERE name = 'sun_ilumya_extract'), 3, 'njb@integrichain.com'),
        ((SELECT id FROM pipeline_state_types WHERE name = 'dimensional'), (SELECT id FROM pipelines WHERE name = 'sun_ilumya_extract'), 4, 'njb@integrichain.com'),

        ((SELECT id FROM pipeline_state_types WHERE name = 'raw'), (SELECT id FROM pipelines WHERE name = 'sun_odomzo_extract'), 0, 'njb@integrichain.com'),
        ((SELECT id FROM pipeline_state_types WHERE name = 'ingest'), (SELECT id FROM pipelines WHERE name = 'sun_odomzo_extract'), 1, 'njb@integrichain.com'),
        ((SELECT id FROM pipeline_state_types WHERE name = 'master'), (SELECT id FROM pipelines WHERE name = 'sun_odomzo_extract'), 2, 'njb@integrichain.com'),
        ((SELECT id FROM pipeline_state_types WHERE name = 'enrich'), (SELECT id FROM pipelines WHERE name = 'sun_odomzo_extract'), 3, 'njb@integrichain.com'),
        ((SELECT id FROM pipeline_state_types WHERE name = 'dimensional'), (SELECT id FROM pipelines WHERE name = 'sun_odomzo_extract'), 4, 'njb@integrichain.com'),

        ((SELECT id FROM pipeline_state_types WHERE name = 'raw'), (SELECT id FROM pipelines WHERE name = 'bi_ofev_patient_status'), 0, 'rns@integrichain.com'),
        ((SELECT id FROM pipeline_state_types WHERE name = 'ingest'), (SELECT id FROM pipelines WHERE name = 'bi_ofev_patient_status'), 1, 'rns@integrichain.com'),
        ((SELECT id FROM pipeline_state_types WHERE name = 'master'), (SELECT id FROM pipelines WHERE name = 'bi_ofev_patient_status'), 2, 'jtobias@integrichain.com'),
        ((SELECT id FROM pipeline_state_types WHERE name = 'enhance'), (SELECT id FROM pipelines WHERE name = 'bi_ofev_patient_status'), 3, 'jtobias@integrichain.com'),
        ((SELECT id FROM pipeline_state_types WHERE name = 'enrich'), (SELECT id FROM pipelines WHERE name = 'bi_ofev_patient_status'), 4, 'jtobias@integrichain.com'),
        ((SELECT id FROM pipeline_state_types WHERE name = 'metrics'), (SELECT id FROM pipelines WHERE name = 'bi_ofev_patient_status'), 5, 'jtobias@integrichain.com'),
        ((SELECT id FROM pipeline_state_types WHERE name = 'dimensional'), (SELECT id FROM pipelines WHERE name = 'bi_ofev_patient_status'), 6, 'jtobias@integrichain.com'),

        ((SELECT id FROM pipeline_state_types WHERE name = 'raw'), (SELECT id FROM pipelines WHERE name = 'alkermes_vivitrol_patient_status'), 0, 'rns@integrichain.com'),
        ((SELECT id FROM pipeline_state_types WHERE name = 'ingest'), (SELECT id FROM pipelines WHERE name = 'alkermes_vivitrol_patient_status'), 1, 'rns@integrichain.com')
        ((SELECT id FROM pipeline_state_types WHERE name = 'master'), (SELECT id FROM pipelines WHERE name = 'alkermes_vivitrol_patient_status'), 2, 'jtobias@integrichain.com'),
        ((SELECT id FROM pipeline_state_types WHERE name = 'enhance'), (SELECT id FROM pipelines WHERE name = 'alkermes_vivitrol_patient_status'), 3, 'jtobias@integrichain.com'),
        ((SELECT id FROM pipeline_state_types WHERE name = 'enrich'), (SELECT id FROM pipelines WHERE name = 'alkermes_vivitrol_patient_status'), 4, 'jtobias@integrichain.com'),
        ((SELECT id FROM pipeline_state_types WHERE name = 'metrics'), (SELECT id FROM pipelines WHERE name = 'alkermes_vivitrol_patient_status'), 5, 'jtobias@integrichain.com'),
        ((SELECT id FROM pipeline_state_types WHERE name = 'dimensional'), (SELECT id FROM pipelines WHERE name = 'alkermes_vivitrol_patient_status'), 6, 'jtobias@integrichain.com');

COMMIT;