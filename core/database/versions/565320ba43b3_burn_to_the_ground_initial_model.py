"""burn-to-the-ground initial model

Revision ID: 565320ba43b3
Revises: 
Create Date: 2019-03-27 15:55:07.183406

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '565320ba43b3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('pharmaceutical_companies',
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('last_actor', sa.String(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('display_name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pipeline_state_types',
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('last_actor', sa.String(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('segments',
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('last_actor', sa.String(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('transformation_templates',
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('last_actor', sa.String(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('variable_structures',sa.String()),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('brands',
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('last_actor', sa.String(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('display_name', sa.String(), nullable=False),
    sa.Column('pharmaceutical_company_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['pharmaceutical_company_id'], ['pharmaceutical_companies.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pipeline_types',
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('last_actor', sa.String(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('segment_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['segment_id'], ['segments.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pipelines',
    sa.Column('is_active', sa.Boolean(), server_default='f',nullable=False),
    sa.Column('description',sa.String(),nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('last_actor', sa.String(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('pipeline_type_id', sa.Integer(), nullable=False),
    sa.Column('brand_id', sa.Integer(), nullable=False),
    sa.Column('run_frequency', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['brand_id'], ['brands.id'], ),
    sa.ForeignKeyConstraint(['pipeline_type_id'], ['pipeline_types.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pipeline_states',
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('last_actor', sa.String(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('pipeline_state_type_id', sa.Integer(), nullable=False),
    sa.Column('pipeline_id', sa.Integer(), nullable=False),
    sa.Column('graph_order', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['pipeline_id'], ['pipelines.id'], ),
    sa.ForeignKeyConstraint(['pipeline_state_type_id'], ['pipeline_state_types.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('transformations',
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('last_actor', sa.String(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('transformation_template_id', sa.Integer(), nullable=False),
    sa.Column('pipeline_state_id', sa.Integer(), nullable=False),
    sa.Column('graph_order', sa.Integer(), server_default=sa.text('0'), nullable=False),
    sa.ForeignKeyConstraint(['pipeline_state_id'], ['pipeline_states.id'], ),
    sa.ForeignKeyConstraint(['transformation_template_id'], ['transformation_templates.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('transformation_variables',
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('last_actor', sa.String(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('transformation_id', sa.Integer(), nullable=False),
    sa.Column('name',sa.String(), nullable=False),
    sa.Column('value',sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['transformation_id'], ['transformations.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    


def downgrade():
    op.drop_table('transformation_variables')
    op.drop_table('transformations')
    op.drop_table('pipeline_states')
    op.drop_table('pipelines')
    op.drop_table('pipeline_types')
    op.drop_table('brands')
    op.drop_table('transformation_templates')
    op.drop_table('segments')
    op.drop_table('pipeline_state_types')
    op.drop_table('pharmaceutical_companies')


