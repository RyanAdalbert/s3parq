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

INSERT INTO pipelines (name, pipeline_type_id, brand_id, run_frequency, last_actor)
    VALUES
        ('bi_just_extract', 
