"""add_run_event

Revision ID: 95ae6c822c97
Revises: 1537c363a63f
Create Date: 2019-06-17 19:46:57.778986

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy import func

# revision identifiers, used by Alembic.
revision = '95ae6c822c97'
down_revision = '1537c363a63f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('run_events',
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=func.now(), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('last_actor', sa.String(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('run_events')
