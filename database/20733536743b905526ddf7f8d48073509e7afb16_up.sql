/* UP! set schemas, triggers and comment on tables created by ORM */

COMMENT ON SCHEMA public IS 'This schema is for all pipeline configurations.';

CREATE SCHEMA IF NOT EXISTS auditing AUTHORIZATION configurator;
COMMENT ON SCHEMA auditing IS 'This schema is for recording changes to the rest of the database.';

CREATE TABLE IF NOT EXISTS auditing.events (
    id SERIAL,
    table_name VARCHAR,
    actor VARCHAR,
    before_value JSONB,
    after_value JSONB,
    event_timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
-- no index on the audit table. keep writes cheap.
-- no constraints, minimize audit risk.


/* Triggers */
-- PL for updated_at
CREATE OR REPLACE FUNCTION public.trigger_updated_at_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END
$$ LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION public.audit_events()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT'
    THEN 
    INSERT INTO auditing.events (table_name, actor, after_value)
    VALUES (TG_TABLE_NAME, NEW.last_actor, to_jsonb(NEW));
    RETURN NEW;

    ELSIF TG_OP = 'UPDATE'
    THEN
    INSERT INTO auditing.events (table_name, actor, before_value, after_value)
    VALUES (TG_TABLE_NAME, NEW.last_actor, to_jsonb(OLD), to_jsonb(NEW));
    RETURN NEW;
    
    ELSIF TG_OP = 'DELETE'
    THEN
        INSERT INTO auditing.events (table_name, actor, before_value)
        VALUES (TG_TABLE_NAME, NEW.last_actor, to_jsonb(OLD));
    RETURN NEW;
    END IF;
END
$$ LANGUAGE 'plpgsql';

/* Table Triggers */

DO $$
DECLARE
    tables CURSOR FOR
        SELECT 
            tablename
        FROM
            pg_tables
        WHERE 
            tablename NOT LIKE 'pg_%' 
        AND 
            tablename NOT LIKE 'sql_%'
        AND 
            schemaname = 'public';
BEGIN
    FOR t IN tables LOOP
        EXECUTE
            '
            DROP TRIGGER IF EXISTS ' || t.tablename || '_updated_at ON public.' || t.tablename || ';
            CREATE TRIGGER ' || t.tablename || '_updated_at 
                BEFORE UPDATE ON public.' || t.tablename ||'
                FOR EACH ROW
                EXECUTE PROCEDURE trigger_updated_at_timestamp();

            DROP TRIGGER IF EXISTS ' || t.tablename || '_audit ON public.' || t.tablename || ';
            CREATE TRIGGER ' || t.tablename || '_audit
                AFTER INSERT OR UPDATE OR DELETE ON public.' || t.tablename || '
                FOR EACH ROW
                EXECUTE PROCEDURE audit_events();';
    END LOOP;
    RETURN;
END
$$
                   
            
/*
CREATE TRIGGER pharmaceutical_companies_updated_at 
    AFTER UPDATE ON pharmaceutical_companies
    EXECUTE PROCEDURE trigger_updated_at_timestamp();

CREATE TRIGGER pharmaceutical_companies_audit
    BEFORE INSERT OR UPDATE OR DELETE ON pharmaceutical_companies
    FOR EACH ROW
    EXECUTE PROCEDURE audit_events();

CREATE TRIGGER pharmaceutical_companies_delete_alt
    BEFORE DELETE ON pharmaceutical_companies
    FOR EACH ROW
    EXECUTE PROCEDURE delete_alt();

COMMENT ON TABLE pharmaceutical_companies IS 'This table represents a pharmaceutical client ie Merck, Pfizer etc.';
COMMENT ON COLUMN pharmaceutical_companies.id IS 'This column is the application-specific unique identifier for a pharmaceutical_company.';
COMMENT ON COLUMN pharmaceutical_companies.name IS 'This column is IntegriChain internal name for a pharmaceutical_company.';
COMMENT ON COLUMN pharmaceutical_companies.display_name IS 'This column is the name used for a pharmaceutical_company in views. May or may not differ from name.';
COMMENT ON COLUMN pharmaceutical_companies.is_active IS 'This column indicates the current status of a pharmaceutical_company. Inactive companies may be excluded from some processes.';
COMMENT ON COLUMN pharmaceutical_companies.is_deleted IS 'Rather than hard-delete records, we set this flag to TRUE to indicate that the record should be ignored.';
COMMENT ON COLUMN pharmaceutical_companies.last_actor IS 'The email address of the most recent IntegriChain user to alter the given record.';
COMMENT ON COLUMN pharmaceutical_companies.created_at IS 'The timestamp the record was created.';
COMMENT ON COLUMN pharmaceutical_companies.updated_at IS 'The timestamp the record was last updated.';

CREATE TRIGGER brands_updated_at 
    AFTER UPDATE ON brands
    EXECUTE PROCEDURE trigger_updated_at_timestamp();

COMMENT ON TABLE brands IS 'This table represents a single brand of a pharmaceutical client ie Viagra, Cialis etc.';
COMMENT ON COLUMN brands.id IS 'This column is the apication-specific unique identifier for a brand.';
COMMENT ON COLUMN brands.name IS 'This column is IntegriChain internal name for a brand.';
COMMENT ON COLUMN brands.display_name IS 'This column is the name used for a brand in views. May or may not differ from name.';
COMMENT ON COLUMN brands.is_active IS 'This column indicates the current status of a brand. Inactive companies may be excluded from some processes.';
COMMENT ON COLUMN brands.is_deleted IS 'Rather than hard-delete records, we set this flag to TRUE to indicate that the record should be ignored.';
COMMENT ON COLUMN brands.last_actor IS 'The email address of the most recent IntegriChain user to alter the given record.';
COMMENT ON COLUMN brands.created_at IS 'The timestamp the record was created.';
COMMENT ON COLUMN brands.updated_at IS 'The timestamp the record was last updated.';

CREATE TRIGGER segments_updated_at 
    AFTER UPDATE ON segments
    EXECUTE PROCEDURE trigger_updated_at_timestamp();

COMMENT ON TABLE segments IS 'This table represents the logical business segments of IntegriChain, ie Payer, Patient, Distribution.';
COMMENT ON COLUMN segments.id IS 'This column is the apication-specific unique identifier for an IntegriChain-defined segment.';
COMMENT ON COLUMN segments.name IS 'This column is IntegriChain internal name for a segment.';
COMMENT ON COLUMN segments.is_active IS 'This column indicates the current status of a brand. Inactive companies may be excluded from some processes.';
COMMENT ON COLUMN segments.is_deleted IS 'Rather than hard-delete records, we set this flag to TRUE to indicate that the record should be ignored.';
COMMENT ON COLUMN segments.last_actor IS 'The email address of the most recent IntegriChain user to alter the given record.';
COMMENT ON COLUMN segments.created_at IS 'The timestamp the record was created.';
COMMENT ON COLUMN segments.updated_at IS 'The timestamp the record was last updated.';

*/
