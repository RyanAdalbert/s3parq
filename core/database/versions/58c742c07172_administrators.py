"""administrators

Revision ID: 58c742c07172
Revises: ce20d3afa35d
Create Date: 2019-04-15 14:06:15.652905

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '58c742c07172'
down_revision = 'ce20d3afa35d'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('administrators',
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('last_actor', sa.String(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email_address', sa.String(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    

def downgrade():
    op.drop_table('administrators')

