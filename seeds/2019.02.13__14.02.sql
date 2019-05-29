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

INSERT INTO transformation_templates (name, variable_structures, pipeline_state_type_id, last_actor) 
    VALUES
        ('extract_from_ftp', 
        '{"filesystem_path":{"datatype": "string", "description": "the remote path to the files"},secret_name":{"datatype":"string","description":"the name of the secret in secret manager"},"prefix":{"datatype":"string","description":"the prefix of the files to get on the remote filesystem"},"secret_type_of":{"datatype":"string","description":"the type of the remote server, used in the secret path"}}', 
        (SELECT id FROM pipeline_state_types WHERE name = 'raw'),
        'rns@integrichain.com');

INSERT INTO pipeline_states (pipeline_state_type_id, pipeline_id, graph_order, last_actor)
    VALUES 
((SELECT id FROM pipeline_state_types WHERE name = 'raw'), (SELECT id FROM pipelines WHERE name = 'bi_init'), 0, 'emk@integrichain.com'),
((SELECT id FROM pipeline_state_types WHERE name = 'raw'), (SELECT id FROM pipelines WHERE name = 'alkermes_init'), 0, 'emk@integrichain.com'),
((SELECT id FROM pipeline_state_types WHERE name = 'raw'), (SELECT id FROM pipelines WHERE name = 'sun_init'), 0, 'emk@integrichain.com');


INSERT INTO transformations (transformation_template_id, pipeline_state_id, graph_order, last_actor)
    VALUES
        ((SELECT id FROM transformation_templates WHERE name = 'extract_from_ftp'),(SELECT id FROM pipeline_states WHERE pipeline_state_type_id = (SELECT id FROM pipeline_state_types WHERE name = 'raw') AND pipeline_id = (SELECT id FROM pipelines WHERE name = 'sun_init')),0, 'emk@integrichain.com'),
        ((SELECT id FROM transformation_templates WHERE name = 'extract_from_ftp'),(SELECT id FROM pipeline_states WHERE pipeline_state_type_id = (SELECT id FROM pipeline_state_types WHERE name = 'raw') AND pipeline_id = (SELECT id FROM pipelines WHERE name = 'alkermes_init')),0, 'emk@integrichain.com'),
        ((SELECT id FROM transformation_templates WHERE name = 'extract_from_ftp'),(SELECT id FROM pipeline_states WHERE pipeline_state_type_id = (SELECT id FROM pipeline_state_types WHERE name = 'raw') AND pipeline_id = (SELECT id FROM pipelines WHERE name = 'bi_init')),0, 'emk@integrichain.com');

INSERT INTO transformation_variables (name, transformation_id, value, last_actor)
    VALUES
        ('filesystem_path',(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'bi_init')) AND id = (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'delimiter' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = "extract_from_ftp")ORDER BY id LIMIT 1))), 'SpecilatyAnalytics', 'rns@integrichain.com'),
        ('prefix',(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'bi_init')) AND id = (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'skip_rows' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = "extract_from_ftp")ORDER BY id LIMIT 1))), 'IPF_PAT_', 'rns@integrichain.com'),
        ('secret_name',(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'bi_init')) AND id = (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'encoding' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = "extract_from_ftp")ORDER BY id LIMIT 1))), 'bi', 'rns@integrichain.com'),
        ('secret_type_of',(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'bi_init')) AND id = (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'input_file_prefix' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = "extract_from_ftp")ORDER BY id LIMIT 1))), 'FTP', 'rns@integrichain.com'),

        ('filesystem_path',(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'bi_init')) AND id = (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'delimiter' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = "extract_from_ftp")ORDER BY id LIMIT 1))), 'SpecilatyAnalytics', 'rns@integrichain.com'),
        ('prefix',(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'bi_init')) AND id = (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'skip_rows' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = "extract_from_ftp")ORDER BY id LIMIT 1))), 'BRIDGE_PAT_', 'rns@integrichain.com'),
        ('secret_name',(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'bi_init')) AND id = (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'encoding' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = "extract_from_ftp")ORDER BY id LIMIT 1))), 'bi', 'rns@integrichain.com'),
        ('secret_type_of',(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'bi_init')) AND id = (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'input_file_prefix' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = "extract_from_ftp")ORDER BY id LIMIT 1))), 'FTP', 'rns@integrichain.com'),

        ('filesystem_path',(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'sun_init')) AND id = (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'delimiter' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = "extract_from_ftp")ORDER BY id LIMIT 1))), 'frommsa/SUN', 'rns@integrichain.com'),
        ('prefix',(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'sun_init')) AND id = (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'skip_rows' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = "extract_from_ftp")ORDER BY id LIMIT 1))), 'INTEGRICHAIN_SUN_', 'rns@integrichain.com'),
        ('secret_name',(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'sun_init')) AND id = (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'encoding' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = "extract_from_ftp")ORDER BY id LIMIT 1))), 'sun', 'rns@integrichain.com'),
        ('secret_type_of',(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'sun_init')) AND id = (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'input_file_prefix' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = "extract_from_ftp")ORDER BY id LIMIT 1))), 'FTP', 'rns@integrichain.com'),

        ('filesystem_path',(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'alkermes_init')) AND id = (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'delimiter' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = "extract_from_ftp")ORDER BY id LIMIT 1))), 'LiquidHub-Achive', 'rns@integrichain.com'),
        ('prefix',(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'alkermes_init')) AND id = (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'skip_rows' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = "extract_from_ftp")ORDER BY id LIMIT 1))), 'VIVITROL_', 'rns@integrichain.com'),
        ('secret_name',(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'alkermes_init')) AND id = (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'encoding' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = "extract_from_ftp")ORDER BY id LIMIT 1))), 'alkermes', 'rns@integrichain.com'),
        ('secret_type_of',(SELECT id FROM transformations WHERE (pipeline_state_id IN (SELECT id FROM pipeline_states WHERE pipeline_id = (SELECT id FROM pipelines WHERE name = 'alkermes_init')) AND id = (SELECT id FROM transformations WHERE (id NOT IN (SELECT t.id FROM transformations t INNER JOIN transformation_variables tv ON t.id = tv.transformation_id WHERE tv.name = 'input_file_prefix' ORDER BY t.id)) AND id IN (SELECT t.id from transformations t INNER JOIN transformation_templates tt ON t.transformation_template_id = tt.id WHERE tt.name = "extract_from_ftp")ORDER BY id LIMIT 1))), 'FTP', 'rns@integrichain.com');