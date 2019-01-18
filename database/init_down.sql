/*  DOWN! Must be connected to postges DB with user other than configurator for Init  */
DROP DATABASE IF EXISTS configuration_application;

DROP ROLE IF EXISTS configurator; 
