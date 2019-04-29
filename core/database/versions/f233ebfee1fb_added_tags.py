"""added tags

Revision ID: f233ebfee1fb
Revises: 58c742c07172
Create Date: 2019-04-29 19:07:49.926123

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f233ebfee1fb'
down_revision = '58c742c07172'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tags',
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('last_actor', sa.String(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('value', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('transformation_templates_tags',
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('last_actor', sa.String(), nullable=True),
    sa.Column('transformation_template_id', sa.Integer(), nullable=False),
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], ),
    sa.ForeignKeyConstraint(['transformation_template_id'], ['transformation_templates.id'], ),
    sa.PrimaryKeyConstraint('transformation_template_id', 'tag_id')
    )

    # ### end Alembic commands ###
    conn = op.get_bind()
    conn.execute("""
                 COMMENT ON TABLE tags IS 'A label used for grouping of other objects (non specific).';
                 COMMENT ON COLUMN tags.value IS 'The textual label of the tag ie current or beta etc.';
                 COMMENT ON TABLE transformation_templates_tags IS 'bridge table between transformation_templates and tags.';
    """)
def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('transformation_templates_tags')
    op.drop_table('tags')
    # ### end Alembic commands ###
