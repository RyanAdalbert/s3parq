BEGIN;
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

    ('ODOMZO', 'ODOMZO', 
        (SELECT 
            id 
        FROM 
            pharmaceutical_companies 
        WHERE 
            name = 'Sun'
    ), 'njb@integrichain.com'),

    ('YONSA', 'YONSA', 
        (SELECT 
            id 
        FROM 
            pharmaceutical_companies 
        WHERE 
            name = 'Sun'
    ), 'njb@integrichain.com'),

    ('All Brands', 'allbrands', 
        (SELECT 
            id 
        FROM 
            pharmaceutical_companies 
        WHERE 
            name = 'Sun'
    ), 'njb@integrichain.com'),

    ('VIVITROL', 'VIVITROL', 
        (SELECT 
            id 
        FROM 
            pharmaceutical_companies 
        WHERE 
            name = 'Alkermes'
    ), 'emk@integrichain.com');

COMMIT;