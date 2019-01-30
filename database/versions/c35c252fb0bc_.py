"""empty message

Revision ID: c35c252fb0bc
Revises: 7333d20cbb08
Create Date: 2019-01-29 13:00:53.459520

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c35c252fb0bc'
down_revision = '7333d20cbb08'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    conn.execute(" COMMENT ON COLUMN extract_configurations.secret_type_of IS 'represents the source type, eg. FTP, databse, S3 etc.';")


def downgrade():
    conn = op.get_bind()
    conn.execute(" COMMENT ON COLUMN extract_configurations.secret_type_of IS '';")
