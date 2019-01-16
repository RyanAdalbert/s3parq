/*  DOWN!   */

DROP DATABASE IF EXISTS configuration_application;

DROP ROLE IF EXISTS configurator; 
CREATE ROLE configurator WITH CREATEDB LOGIN;
GRANT configurator to postgres;

CREATE DATABASE configuration_application WITH OWNER configurator;

SET ROLE 'configurator';

EXEC SQL SET CONNECTION TO configuration_application;

CREATE SCHEMA configuration AUTHORIZATION configurator;

SET SCHEMA 'configuration';


/* Table DDL */
CREATE TABLE pharmaceutical_companies (
  id SERIAL PRIMARY KEY,
  name VARCHAR NOT NULL UNIQUE,
  display_name VARCHAR NOT NULL UNIQUE,
  is_active BOOLEAN DEFAULT TRUE,
  is_deleted BOOLEAN DEFAULT FALSE
);

CREATE INDEX "pharmaceutical_companies_id" ON pharmaceutical_companies ("id");
