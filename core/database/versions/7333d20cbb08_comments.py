"""comments

Revision ID: 7333d20cbb08
Revises: 1134cec79e78
Create Date: 2019-01-20 18:48:50.863496

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7333d20cbb08'
down_revision = '1134cec79e78'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    conn.execute("""
        CREATE OR REPLACE FUNCTION create_table_comments()
        RETURNS event_trigger
        LANGUAGE plpgsql
        AS $$
        DECLARE
            obj record;    
        BEGIN
          FOR obj IN SELECT * FROM pg_event_trigger_ddl_commands() WHERE command_tag in ('SELECT INTO','CREATE TABLE','CREATE TABLE AS')
          LOOP
            EXECUTE'
                    COMMENT ON COLUMN ' || obj.object_identity ||'.updated_at IS ''represents the most recent DML operation timestamp for a row.'';
                    COMMENT ON COLUMN ' || obj.object_identity ||'.created_at IS ''represents the timestamp a row was initially created.'';
                    COMMENT ON COLUMN ' || obj.object_identity ||'.last_actor IS ''represents the most recent user email to update or insert this row.'';
                 '; END LOOP;
        END;
        $$;

        CREATE EVENT TRIGGER common_comments ON ddl_command_end
        WHEN TAG IN ('SELECT INTO','CREATE TABLE','CREATE TABLE AS')
        EXECUTE PROCEDURE create_table_comments();

        COMMENT ON FUNCTION public.create_table_comments IS 'applies common object comments to created_at, updated_at and last_actor columns.';
    """
    )

def downgrade():
    conn = op.get_bind()
    conn.execute('DROP FUNCTION create_table_comments CASCADE;')
