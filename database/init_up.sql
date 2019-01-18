/* UP! Inital creation of the database and role. Must be connected to database postgres. */

-- set password as part of deployment
CREATE ROLE configurator WITH LOGIN;

CREATE DATABASE configuration_application WITH OWNER configurator;
COMMENT ON DATABASE configuration_application IS 
    'This database is the source for configuration settings for the Core pipeline. https://github.com/IntegriChain1/core.';

COMMENT ON ROLE configurator IS 'This role is used for all configuration_application DDL operations.';
