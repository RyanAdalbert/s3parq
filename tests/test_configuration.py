import pytest
import core.configuration  as config

def test_get_extract_configuration():
    session = config._dev_in_memory()
    ## make dummy records
    ec = config.ExtractConfiguration
    t = config.Transformation
    session.add(t(id=1))
    session.commit()
   
    test_secret_names = []    
    for x in range(0,3):
        sname = f'test_secret_{x}'
        session.add(ec(transformation_id = 1, 
                    secret_name = sname))
        test_secret_names.append(sname)

    session.commit()
    
    q = session.query(t).filter(t.id == 1)    
    secrets = []   
    for f_transform in q:
        for extract in f_transform.extract_configurations:
            secrets.append(extract.secret_name)

    assert set(test_secret_names) == set(secrets)
