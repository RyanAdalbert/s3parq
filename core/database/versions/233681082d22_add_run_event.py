"""add_run_event

Revision ID: 233681082d22
Revises: 1537c363a63f
Create Date: 2019-06-18 15:10:17.960451

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '233681082d22'
down_revision = '1537c363a63f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('run_events',
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now(), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('last_actor', sa.String(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('pipeline_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['pipeline_id'], ['pipelines.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    

def downgrade():
    op.drop_table('run_events')
