-- SQL commands for setting up an RDS instance to work with Core
-- This should only need to be set up once, on initial RDS creation

CREATE ROLE configurator WITH  LOGIN PASSWORD '{some password}';
GRANT rds_superuser TO configurator;

CREATE DATABASE configuration_application;
ALTER DATABASE configuration_application OWNER TO configurator;
ALTER SCHEMA public OWNER TO configurator;