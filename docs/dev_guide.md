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

    # using configurations
    from core.helpers.configuration_mocker import ConfigurationMocker as CMock
    import core.models.configuration as config
    
    ## creates the mock db
    mock = CMock()
    session = mock.get_session()

    ## uses the config entity classes
    transform_template = config.TransformationTemplate

    ## you can seed the db
    mock.generate_mocks()
    
    total = session.query(transform_template).count()
    print(total)
    ## 2

    ## you can also add entities as you need them
    session.add(transform_template(name='great_new_transform_template'))
    session.commit()

    added = session.query(transform_template).order_by(transform_template.id.desc()).first()
    print(added.name)
    ## 'great_new_transform_template'

    new_total = session.query(transform_template).count()
    print(total)
    ## 3

However, this is _not_ the same thing as the production database environment - Sqlite does not support our PL Postgres functions, triggers etc. To get this full functionality in development you have 2 options:
- point to a Development / UAT / Production configuration\_application instance:
When you are making no changes to the config schema and just need to read, you can do this using the Secret module.

- point to a local PG instance and run the migration suite:
this will give you a full local build that you can then modify, create new migrations for etc. 

### Migrations
we use [alembic](https://pypi.org/project/alembic/) to manage migrations for the configuration application. This assumes you have:
- a running PG instance at localhost:5432 
- a database configuration\_application 
- a pg user configurator with password configurator, who owns this database and the PUBLIC schema 

Basic use is:
    
    ## apply all migrations and bring DB up to speed
    >>>MAC: database YOU$ alembic upgrade head

    ## generate a blank migration for PL stuff
    >>>MAC: database YOU$ alembic revision -m "added default trigger"  
 
    ## auto-generate a completed DDL migration based on the diff between your model and the DB
    >>>MAC: database YOU$ alembic revision --autogenerate -m "added table hamburger_salad"

### Credentials
login creds, host URLS, and other security-minded bits are managed by aws secretsmanager. To access these you can use the `Secret` class. 

    from core.secret import Secret
    s = Secret( name='hamburger',
                type_of='FTP',
                env='dev',
                mode='read')
    s.password
    ## returns hamburger_password 

Note that env should be passed from some environment-aware variable.    

### Corebot
Corebot is another CLI interface. This is meant to be the "client" part to our "server" part, allowing a separate interface for what people should be calling vs. what processes should be calling. This should only be the entry point, with the guts of the processes still living in a component in standard core.
