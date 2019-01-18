# Dev Guide

## Running Scripts

This project uses the idea of having basic (mostly) scripts to do tasks like testing, building, and serving applications - this idea was taken from https://github.com/github/scripts-to-rule-them-all. These scripts live in the /script directory and MUST be executed from the base directory of this repository.

## Getting Started
### Configurations 
**Why?** 
All pipelines need configurations. These range from the name of the client to the order of transformations to be applied. 
We manage these configurations via a configuration application, which in turn stores them in an RDMBS. To acces these configurations you use the [Configurations module](../core/models/configuration.py)

You use [SQLAlchemy Sessions](https://docs.sqlalchemy.org/en/rel_1_2/orm/tutorial.html#querying) to query that class.
In development it can be useful to get the functionality without setting up and migrating a database, so we have a helper class that builds an in-memory sqlite instance and can populate mock data. 
    import core.helpers.configuration_mocker as CMock
    import core.models.configuration as config
    
    ## creates the mock db
    mock = CMock()
    session = mock.get_session()

    ## uses the config entity classes
    transform_template = config.TransformationTemplate
    
    ## you can add entities as you need them
    session.add(transform_template(name='great_new_transform_template'))
    session.commit()

    added = session.query(transform_template).first()
    print(added.name)
    ## 'great_new_transform_template'

    ## you can also seed the db
    mock.generate_mocks()

    total = session.query(transform_template).count()
    print(total)
    ## 4
