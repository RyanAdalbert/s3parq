INSERT INTO 
    pharmaceutical_companies (display_name, name, last_actor) 
VALUES 
    ('Boehringer Ingelheim', 'BI', 'emk@integrichain.com'),
    ('Sun Pharmaceutical Industries Ltd.', 'Sun', 'emk@integrichain.com'),
    ('Alkermes', 'Alkermes', 'emk@integrichain.com');


INSERT INTO 
    brands (display_name, name, pharmaceutical_company_id, last_actor)
VALUES
    ('OFEV', 'OFEV', 
        (SELECT 
            id 
        FROM 
            pharmaceutical_companies 
        WHERE 
            name = 'BI'
    ), 'emk@integrichain.com'),

    ('ILUMYA', 'ILUMYA', 
        (SELECT 
            id 
        FROM 
            pharmaceutical_companies 
        WHERE 
            name = 'Sun'
    ), 'emk@integrichain.com'),

    ('VIVITROL', 'VIVITROL', 
        (SELECT 
            id 
        FROM 
            pharmaceutical_companies 
        WHERE 
            name = 'Alkermes'
    ), 'emk@integrichain.com');

INSERT INTO pipeline_state_types (name, last_actor)
    VALUES  ('raw','emk@integrichain.com'),
            ('ingest','emk@integrichain.com'),
            ('master','emk@integrichain.com'),
            ('enhance','emk@integrichain.com'),
            ('enrich','emk@integrichain.com'),
            ('metrics','emk@integrichain.com'),
            ('dimensional','emk@integrichain.com');

INSERT INTO segments (name, last_actor)
    VALUES  ('patient','emk@integrichain.com'),
            ('payer','emk@integrichain.com'),
            ('distribution','emk@integrichain.com');

INSERT INTO pipeline_types (name, segment_id, last_actor)
    VALUES  ('EDO',(SELECT id FROM segments WHERE name = 'distribution'),'emk@integrichain.com'),
            ('patient_journey',(SELECT id FROM segments WHERE name = 'patient'),'emk@integrichain.com');

INSERT INTO pipelines (name, is_active, description, pipeline_type_id, brand_id, run_frequency, last_actor)
    VALUES
        ('bi_just_extract', TRUE, 'initial extract-only pipeline for BI.', (SELECT id FROM pipeline_types WHERE name = 'patient_journey'), (SELECT id from brands WHERE name = 'OFEV'), 'weekly', 'emk@integrichain.com'),
        ('sun_just_extract', TRUE, 'initial extract-only pipeline for Sun.', (SELECT id FROM pipeline_types WHERE name = 'patient_journey'), (SELECT id from brands WHERE name = 'ILUMYA'), 'daily', 'emk@integrichain.com'),
        ('alkermes_just_extract', TRUE, 'initial extract-only pipeline for Alkermes.', (SELECT id FROM pipeline_types WHERE name = 'patient_journey'), (SELECT id from brands WHERE name = 'VIVITROL'), 'weekly', 'emk@integrichain.com');

INSERT INTO transformation_templates (name, last_actor) 
    VALUES
        ('extract_from_ftp','emk@integrichain.com');

INSERT INTO pipeline_states (pipeline_state_type_id, pipeline_id, graph_order, last_actor)
    VALUES 
((SELECT id FROM pipeline_state_types WHERE name = 'raw'), (SELECT id FROM pipelines WHERE name = 'bi_just_extract'), 0, 'emk@integrichain.com'),
((SELECT id FROM pipeline_state_types WHERE name = 'raw'), (SELECT id FROM pipelines WHERE name = 'sun_just_extract'), 0, 'emk@integrichain.com'),
((SELECT id FROM pipeline_state_types WHERE name = 'raw'), (SELECT id FROM pipelines WHERE name = 'alkermes_just_extract'), 0, 'emk@integrichain.com');


INSERT INTO transformations (transformation_template_id, pipeline_state_id, graph_order, last_actor)
    VALUES
        ((SELECT id FROM transformation_templates WHERE name = 'extract_from_ftp'),(SELECT id FROM pipeline_states WHERE pipeline_state_type_id = (SELECT id FROM pipeline_state_types WHERE name = 'raw') AND pipeline_id = (SELECT id FROM pipelines WHERE name = 'sun_just_extract')),0, 'emk@integrichain.com'),
        ((SELECT id FROM transformation_templates WHERE name = 'extract_from_ftp'),(SELECT id FROM pipeline_states WHERE pipeline_state_type_id = (SELECT id FROM pipeline_state_types WHERE name = 'raw') AND pipeline_id = (SELECT id FROM pipelines WHERE name = 'alkermes_just_extract')),0, 'emk@integrichain.com'),
        ((SELECT id FROM transformation_templates WHERE name = 'extract_from_ftp'),(SELECT id FROM pipeline_states WHERE pipeline_state_type_id = (SELECT id FROM pipeline_state_types WHERE name = 'raw') AND pipeline_id = (SELECT id FROM pipelines WHERE name = 'bi_just_extract')),0, 'emk@integrichain.com');

INSERT INTO extract_configurations (transformation_id, secret_name, secret_type_of, filesystem_path, prefix, last_actor)
    VALUES
        ((SELECT id FROM transformations WHERE transformation_template_id = (SELECT id FROM transformation_templates WHERE name = 'extract_from_ftp') AND pipeline_state_id = (SELECT id FROM pipeline_states WHERE pipeline_state_type_id = (SELECT id FROM pipeline_state_types WHERE name = 'raw') AND pipeline_id = (SELECT id FROM pipelines WHERE name = 'sun_just_extract'))), 
        'sun',
        'FTP',
        'frommsa/SUN',
        'INTEGRICHAIN_SUN_',
        'emk@integrichain.com'),
        ((SELECT id FROM transformations WHERE transformation_template_id = (SELECT id FROM transformation_templates WHERE name = 'extract_from_ftp') AND pipeline_state_id = (SELECT id FROM pipeline_states WHERE pipeline_state_type_id = (SELECT id FROM pipeline_state_types WHERE name = 'raw') AND pipeline_id = (SELECT id FROM pipelines WHERE name = 'bi_just_extract'))), 
        'bi',
        'FTP',
        'SpecilatyAnalytics',
        'IPF_PAT_',
        'emk@integrichain.com'),
        ((SELECT id FROM transformations WHERE transformation_template_id = (SELECT id FROM transformation_templates WHERE name = 'extract_from_ftp') AND pipeline_state_id = (SELECT id FROM pipeline_states WHERE pipeline_state_type_id = (SELECT id FROM pipeline_state_types WHERE name = 'raw') AND pipeline_id = (SELECT id FROM pipelines WHERE name = 'bi_just_extract'))), 
        'bi',
        'FTP',
        'SpecilatyAnalytics',
        'BRIDGE_PAT_',
        'emk@integrichain.com'),
        ((SELECT id FROM transformations WHERE transformation_template_id = (SELECT id FROM transformation_templates WHERE name = 'extract_from_ftp') AND pipeline_state_id = (SELECT id FROM pipeline_states WHERE pipeline_state_type_id = (SELECT id FROM pipeline_state_types WHERE name = 'raw') AND pipeline_id = (SELECT id FROM pipelines WHERE name = 'alkermes_just_extract'))), 
        'alkermes',
        'FTP',
        'LiquidHub-Achive',
        'VIVITROL_',
        'emk@integrichain.com');
