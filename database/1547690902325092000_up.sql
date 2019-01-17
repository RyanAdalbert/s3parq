SET SCHEMA 'configuration';

/* Trigger PL for updated_at */
CREATE OR REPLACE FUNCTION trigger_updated_at_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language plpgsql;


/* Table DDL */
CREATE TABLE pharmaceutical_companies (
  id SERIAL PRIMARY KEY,
  name VARCHAR NOT NULL UNIQUE,
  display_name VARCHAR NOT NULL UNIQUE,
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
  last_actor VARCHAR,
  created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
  updated_at TIMESTAMPTZ DEFAULT NOW() NOT NULL  
);

CREATE INDEX "pharmaceutical_companies_id" ON pharmaceutical_companies ("id");

CREATE TRIGGER pharmaceutical_companies_updated_at 
    AFTER UPDATE ON pharmaceutical_companies
    EXECUTE PROCEDURE trigger_updated_at_timestamp();

COMMENT ON TABLE pharmaceutical_companies IS 'This table represents a pharmaceutical client ie Merck, Pfizer etc.';
COMMENT ON COLUMN pharmaceutical_companies.id IS 'This column is the application-specific unique identifier for a pharmaceutical_company.';
COMMENT ON COLUMN pharmaceutical_companies.name IS 'This column is IntegriChain internal name for a pharmaceutical_company.';
COMMENT ON COLUMN pharmaceutical_companies.display_name IS 'This column is the name used for a pharmaceutical_company in views. May or may not differ from name.';
COMMENT ON COLUMN pharmaceutical_companies.is_active IS 'This column indicates the current status of a pharmaceutical_company. Inactive companies may be excluded from some processes.';
COMMENT ON COLUMN pharmaceutical_companies.is_deleted IS 'Rather than hard-delete records, we set this flag to TRUE to indicate that the record should be ignored.';
COMMENT ON COLUMN pharmaceutical_companies.last_actor IS 'The email address of the most recent IntegriChain user to alter the given record.';
COMMENT ON COLUMN pharmaceutical_companies.created_at IS 'The timestamp the record was created.';
COMMENT ON COLUMN pharmaceutical_companies.updated_at IS 'The timestamp the record was last updated.';


CREATE TABLE brands (
  id SERIAL PRIMARY KEY,
  name VARCHAR NOT NULL UNIQUE,
  display_name VARCHAR NOT NULL UNIQUE,
  pharmaceutical_company_id INT NOT NULL REFERENCES pharmaceutical_companies(id),
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  run_frequency VARCHAR,
  is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
  last_actor VARCHAR,
  created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
  updated_at TIMESTAMPTZ DEFAULT NOW() NOT NULL  
);

CREATE INDEX "brands_id" ON  brands ("id");
CREATE INDEX "brands_name" ON  "brands" ("name");

COMMENT ON TABLE brands IS 'This table represents a single brand of a pharmaceutical client ie Viagra, Cialis etc.';
COMMENT ON COLUMN brands.id IS 'This column is the apication-specific unique identifier for a brand.';
COMMENT ON COLUMN brands.name IS 'This column is IntegriChain internal name for a brand.';
COMMENT ON COLUMN brands.display_name IS 'This column is the name used for a brand in views. May or may not differ from name.';
COMMENT ON COLUMN brands.is_active IS 'This column indicates the current status of a brand. Inactive companies may be excluded from some processes.';
COMMENT ON COLUMN brands.is_deleted IS 'Rather than hard-delete records, we set this flag to TRUE to indicate that the record should be ignored.';
COMMENT ON COLUMN brands.last_actor IS 'The email address of the most recent IntegriChain user to alter the given record.';
COMMENT ON COLUMN brands.created_at IS 'The timestamp the record was created.';
COMMENT ON COLUMN brands.updated_at IS 'The timestamp the record was last updated.';

CREATE TRIGGER brands_updated_at 
    AFTER UPDATE ON brands
    EXECUTE PROCEDURE trigger_updated_at_timestamp();


CREATE TABLE segments (
  id SERIAL PRIMARY KEY,
  name VARCHAR NOT NULL UNIQUE,
  is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  last_actor VARCHAR,
  created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
  updated_at TIMESTAMPTZ DEFAULT NOW() NOT NULL  
);

COMMENT ON TABLE segments IS 'This table represents the logical business segments of IntegriChain, ie Payer, Patient, Distribution.';
COMMENT ON COLUMN segments.id IS 'This column is the apication-specific unique identifier for an IntegriChain-defined segment.';
COMMENT ON COLUMN segments.name IS 'This column is IntegriChain internal name for a segment.';
COMMENT ON COLUMN segments.is_active IS 'This column indicates the current status of a brand. Inactive companies may be excluded from some processes.';
COMMENT ON COLUMN segments.is_deleted IS 'Rather than hard-delete records, we set this flag to TRUE to indicate that the record should be ignored.';
COMMENT ON COLUMN segments.last_actor IS 'The email address of the most recent IntegriChain user to alter the given record.';
COMMENT ON COLUMN segments.created_at IS 'The timestamp the record was created.';
COMMENT ON COLUMN segments.updated_at IS 'The timestamp the record was last updated.';


CREATE TRIGGER segments_updated_at 
    AFTER UPDATE ON segments
    EXECUTE PROCEDURE trigger_updated_at_timestamp();

/*
CREATE TABLE "pipeline_types" (
  "id" int,
  "name" varchar,
  "segment_id" int,
  "is_deleted" bool,
  PRIMARY KEY ("id")
);

CREATE INDEX " " ON  "pipeline_types" ("name", "segment_id", "is_deleted");

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
*/
