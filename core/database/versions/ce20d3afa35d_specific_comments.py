"""specific comments

Revision ID: ce20d3afa35d
Revises: e7f82f654287
Create Date: 2019-03-27 16:20:11.846161

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ce20d3afa35d'
down_revision = 'e7f82f654287'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    conn.execute("""
                 COMMENT ON TABLE pharmaceutical_companies IS 'A single business acting as a client to IntegriChain.';
                 COMMENT ON TABLE brands IS 'A single offering of a pharmaceutical company, most often a drug or medication.';
                 COMMENT ON TABLE segments IS 'The business unit within IntegriChain, one of patient, payer, or distribution.';
                 COMMENT ON TABLE pipeline_types IS 'An abstract grouping of pipelines by similar purpose, ie edo, extract_only etc.';
                 COMMENT ON TABLE pipelines IS 'A single instance of a pipeline type comprised of ordered states.';
                 COMMENT ON TABLE pipeline_states IS 'A single instance of a pipeline state type comprised of ordered transform tasks.';
                 COMMENT ON TABLE pipeline_state_types IS 'An abstract grouping of pipeline states, one of: raw, ingest, master, enrich, enhance, metrics, dimensional.';
                 COMMENT ON TABLE transformations IS 'A single instance of a transformation template, ie abc_unblind would be a transformation_template, abc_unblind_veritrol would be a transformation.';
                 COMMENT ON TABLE transformation_templates IS 'An abstract group of transformations, usually 1:1 with a Jupyter Notebook, ie abc_unblind would be a transformation_template, abc_unblind_veritrol would be a transformation.';


                -- COLUMNS 
                   
                COMMENT ON COLUMN segments.name IS 'The business divison of IntegriChain. Expected values are Distribution, Patient and Payer.';
                COMMENT ON COLUMN pipeline_states.graph_order IS 'The wave number of the pipeline state. States are executed in ascending numeric wave order, with equal wave values executing in parallel.';
                COMMENT ON COLUMN pipelines.run_frequency IS 'The airflow-supported run frequency as a string (without the @ symbol). Expected values are weekly, monthly, hourly, daily, none, yearly. See https://airflow.apache.org/scheduler.html#dag-runs for more information.';
                COMMENT ON COLUMN pipeline_state_types.name IS 'One of raw, ingest, master, enhance, enrich, metrics, dimensional.';
                COMMENT ON COLUMN transformations.graph_order IS 'The wave number of the transformation within a given pipeline state. Transforms are executed in ascending numeric wave order, with equal wave values executing in parallel.';
                COMMENT ON COLUMN transformation_templates.name IS 'The human readable descriptive identifier of the transformation template.';
            
    """)

def downgrade():
    conn = op.get_bind()
    conn.execute("""
                 COMMENT ON TABLE pharmaceutical_companies IS '';
                 COMMENT ON TABLE brands IS '';
                 COMMENT ON TABLE segments IS '';
                 COMMENT ON TABLE pipeline_types IS '';
                 COMMENT ON TABLE pipelines IS '':
                 COMMENT ON TABLE pipeline_states IS '':
                 COMMENT ON TABLE pipeline_state_typess IS '':
                 COMMENT ON TABLE transformations IS '':
                 COMMENT ON TABLE transformation_templates IS '':
    
                -- COLUMNS 
                   
                COMMENT ON COLUMN segments.name IS '';
                COMMENT ON COLUMN pipeline_states.graph_order IS '';
                COMMENT ON COLUMN pipelines.run_frequency IS '';
                COMMENT ON COLUMN pipeline_state_types.name IS '';
                COMMENT ON COLUMN transformations.graph_order IS '';
                COMMENT ON COLUMN transformation_templates.name IS '';
            
    """)
