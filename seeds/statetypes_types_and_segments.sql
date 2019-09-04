BEGIN;

INSERT INTO pipeline_state_types (name, last_actor)
    VALUES  
    ('raw','emk@integrichain.com'),
    ('ingest','emk@integrichain.com'),
    ('master','emk@integrichain.com'),
    ('enhance','emk@integrichain.com'),
    ('enrich','emk@integrichain.com'),
    ('metrics','emk@integrichain.com'),
    ('dimensional','emk@integrichain.com');

INSERT INTO segments (name, last_actor)
    VALUES  
    ('patient','emk@integrichain.com'),
    ('payer','emk@integrichain.com'),
    ('distribution','emk@integrichain.com');

INSERT INTO pipeline_types (name, segment_id, last_actor)
    VALUES  
    ('EDO',(SELECT id FROM segments WHERE name = 'distribution'),'emk@integrichain.com'),
    ('patient_journey',(SELECT id FROM segments WHERE name = 'patient'),'emk@integrichain.com');

COMMIT;