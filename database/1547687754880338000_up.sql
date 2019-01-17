/* UP! Create the base schemas */

/* Schema DDL*/
CREATE SCHEMA configuration AUTHORIZATION configurator;
COMMENT ON SCHEMA configuration IS 'This schema is for all pipeline configurations.';

CREATE SCHEMA auditing AUTHORIZATION configurator;
COMMENT ON SCHEMA auditing IS 'This schema is for recording changes to the rest of the database.';




