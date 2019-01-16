/* UP!
*/

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
/*


CREATE TABLE "pipeline_state_transformations" (
  "pipeline_state_id" int,
  "transformation_id" int,
  "graph_order" int
);

CREATE INDEX "FK" ON  "pipeline_state_transformations" ("pipeline_state_id", "transformation_id");

CREATE INDEX " " ON  "pipeline_state_transformations" ("graph_order");

CREATE TABLE "brands" (
  "id" int,
  "name" varchar,
  "display_name" varchar,
  "pharmaceutical_company_id" int,
  "is_active" bool,
  "run_frequency" varchar,
  "is_deleted" bool,
  PRIMARY KEY ("id")
);

CREATE INDEX "U" ON  "brands" ("name", "display_name");

CREATE INDEX "FK" ON  "brands" ("pharmaceutical_company_id");

CREATE INDEX " " ON  "brands" ("is_active", "run_frequency", "is_deleted");

CREATE TABLE "transformations" (
  "id" int ,
  "name" varchar,
  "is_active" bool,
  "is_deleted" bool,
  PRIMARY KEY ("id")
);

CREATE INDEX " " ON  "transformations" ("name", "is_active", "is_deleted");


CREATE TABLE "pipeline_states" (
  "id" int ,
  "name" varchar,
  "pipeline_id" int,
  "graph_order" int,
  "pipeline_state_type_id" int,
  "is_active" bool,
  "is_deleted" bool,
  PRIMARY KEY ("id")
);

CREATE INDEX "U" ON  "pipeline_states" ("name", "graph_order");

CREATE INDEX "FK" ON  "pipeline_states" ("pipeline_id", "pipeline_state_type_id");

CREATE INDEX " " ON  "pipeline_states" ("is_active", "is_deleted");

CREATE TABLE "segments" (
  "id" int,
  "name" varchar,
  "is_deleted" bool,
  PRIMARY KEY ("id")
);

CREATE INDEX " " ON  "segments" ("name", "is_deleted");

CREATE TABLE "pipelines" (
  "id" int,
  "display_name" varchar,
  "pipeline_type_id" int,
  "brand_id" int,
  "is_active" bool,
  "run_frequency" varchar,
  "is_deleted" bool,
  PRIMARY KEY ("id")
);

CREATE INDEX "FK" ON  "pipelines" ("pipeline_type_id", "brand_id");

CREATE INDEX " " ON  "pipelines" ("is_active", "run_frequency", "is_deleted");

CREATE TABLE "pipeline_types" (
  "id" int,
  "name" varchar,
  "segment_id" int,
  "is_deleted" bool,
  PRIMARY KEY ("id")
);

CREATE INDEX " " ON  "pipeline_types" ("name", "segment_id", "is_deleted");

CREATE TABLE "source_path_sets" (
  "id" int,
  "pipeline_state_id" int,
  "filesystem_path" varchar,
  "prefix" varchar,
  "is_active" bool,
  "is_deleted" bool,
  PRIMARY KEY ("id")
);

CREATE INDEX "FK" ON  "source_path_sets" ("pipeline_state_id");

CREATE INDEX " " ON  "source_path_sets" ("filesystem_path", "prefix", "is_active", "is_deleted");

CREATE TABLE "pipeline_state_types" (
  "id" int,
  "name" varchar,
  "is_active" bool,
  "is_deleted" bool,
  PRIMARY KEY ("id")
);

CREATE INDEX "U" ON  "pipeline_state_types" ("name");

CREATE INDEX " " ON  "pipeline_state_types" ("is_active");

*/
