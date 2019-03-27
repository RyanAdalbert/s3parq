"""audit_db_and_triggers

Revision ID: 41cbaa495f77
Revises: 565320ba43b3
Create Date: 2019-03-27 16:10:04.757035

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '41cbaa495f77'
down_revision = '565320ba43b3'
branch_labels = None
depends_on = None



def upgrade():
    conn = op.get_bind()
    
    conn.execute("""
        /* set schemas, triggers and comment on tables created by ORM */

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
                    tablename NOT LIKE 'pg_%%' 
                AND 
                    tablename NOT LIKE 'sql_%%'
                AND 
                    tablename <> 'alembic_version'
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
        """
    )


def downgrade():
    conn = op.get_bind()
    
    conn.execute("""
        DROP FUNCTION public.trigger_updated_at_timestamp CASCADE;
        DROP FUNCTION public.audit_events CASCADE;
        DROP FUNCTION public.delete_alt CASCADE;
        DROP SCHEMA auditing CASCADE;
        """
    )

