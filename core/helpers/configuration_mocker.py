from sqlalchemy.orm.session import Session
from sqlalchemy import create_engine
import core.models.configuration as config
from core.logging import LoggerMixin


class ConfigurationMocker(LoggerMixin):
    """ for development, creates in-memory database instance and a matching session and 
        gives you a bunch of mocked data.
        NOTE: This generates the models directly from the core.models.configuration.py model classes, 
        and could potentially differ from alembic migrations. 
    """

    def __init__(self)-> None:
        engine = config.GenerateEngine(in_memory=True).get_engine()

        # this instansiates the in-memory sqlite instance
        config.Base.metadata.create_all(engine)

        session = config.Session(engine)
        self.session = session.get_session()

    def get_session(self) -> Session:
        return self.session

    def generate_mocks(self)-> None:
        self._mock_administrators()
        self._mock_pharmaceutical_companies()
        self._mock_brands()
        self._mock_segments()
        self._mock_pipeline_types()
        self._mock_pipelines()
        self._mock_pipeline_state_types()
        self._mock_pipeline_states()
        self._mock_tags()
        self._mock_transformation_templates()
        self._mock_transformation_templates_tags()
        self._mock_transformations()
        self._mock_transformation_variables()

    def _mock_transformation_templates_tags(self)->None:
        self.logger.debug('Generating bridge table mocks for transformation_templates <=> tags.')
        t = config.TransformationTemplateTag
        self.session.add_all([
            t(transformation_template_id = 1, tag_id = 1),
            t(transformation_template_id = 2, tag_id = 1),
            t(transformation_template_id = 1, tag_id = 2)
        ])
        self.session.commit()
        self.logger.debug('Done generating transformation_templates_tags mocks.')

    def _mock_tags(self)->None:
        self.logger.debug('Generating tag mocks.')
        t = config.Tag
        self.session.add_all([
            t(id=1, value = 'current'),
            t(id=2, value = 'deprecated'),
            t(id=3, value = 'beta')
        ])
        self.session.commit()
        self.logger.debug('Done generating tag mocks.')
    
    def _mock_administrators(self)->None:
        self.logger.debug('Generating administrator mocks.')
        a = config.Administrator
        self.session.add_all([
            a(id=1, first_name = "Fox", last_name = "Mulder", email_address="fwm@integrichain.com"),
            a(id=2, first_name = "Dana", last_name = "Skully", email_address="dks@integrichain.com"),
            a(id=3, first_name = "Alec", last_name="Wertheimer", email_address="ajw@integrichain.com"),
            a(id=4, first_name = "Natie", last_name="Bohnel", email_address="njb@integrichain.com")
        ])
        self.session.commit()
        self.logger.debug('Done generating administrator mocks.')
        
    def _mock_brands(self)-> None:
        self.logger.debug('Generating brand mocks.')
        b = config.Brand
        self.session.add_all([
            b(id=1, name="Teamocil", display_name="Teamocil",
              pharmaceutical_company_id=1),
            b(id=2, name="Cornballer", display_name="Corn Baller", pharmaceutical_company_id=2)])
        self.session.commit()
        self.logger.debug('Done generating brand mocks.')

    def _mock_pharmaceutical_companies(self)-> None:
        self.logger.debug('Generating pharmaceutical company mocks.')
        p = config.PharmaceuticalCompany
        self.session.add_all([
            p(id=1, display_name="Natural Life Food Company", name='Nfoods'),
            p(id=2, display_name="Sitwell Home Construction", name="Sitwell")])
        self.session.commit()
        self.logger.debug('Done generating pharmaceutical company mocks.')

    def _mock_pipelines(self)-> None:
        self.logger.debug('Generating pipeline mocks.')
        p = config.Pipeline
        self.session.add_all([
            p(id=1, name="bluth_banana_regression", brand_id=2,
              pipeline_type_id=1, run_frequency='daily'),
            p(id=2, name="bluth_profitability", brand_id=2,
              pipeline_type_id=2, run_frequency='hourly'),
            p(id=3, name="temocil_profitablility", brand_id=1,
              pipeline_type_id=1, run_frequency='daily'),
            p(id=500, name="bluth_banana_regression_deprecated", brand_id=2,
              pipeline_type_id=1, is_active=False, run_frequency='hourly')])
        self.session.commit()
        self.logger.debug('Done generating pipeline mocks.')

    def _mock_pipeline_states(self)-> None:
        self.logger.debug('Generating pipeline state mocks.')
        p = config.PipelineState
        self.session.add_all([
            p(id=1, pipeline_state_type_id=1, pipeline_id=1, graph_order=0),
            p(id=2, pipeline_state_type_id=2, pipeline_id=1, graph_order=1),
            p(id=3, pipeline_state_type_id=3, pipeline_id=1, graph_order=2),
            p(id=4, pipeline_state_type_id=1, pipeline_id=2, graph_order=0)])
        self.session.commit()
        self.logger.debug('Done generating pipeline state mocks.')

    def _mock_pipeline_state_types(self)-> None:
        self.logger.debug('Generating pipeline state type mocks.')
        p = config.PipelineStateType
        self.session.add_all([
            p(id=1, name="raw"),
            p(id=2, name="ingest"),
            p(id=3, name="master"),
            p(id=4, name="enhance"),
            p(id=5, name="enrich"),
            p(id=6, name="metrics"),
            p(id=7, name="dimensional")])
        self.session.commit()
        self.logger.debug('Done generating pipeline state type mocks.')

    def _mock_pipeline_types(self)-> None:
        self.logger.debug('Generating pipeline type mocks.')
        p = config.PipelineType
        self.session.add_all([
            p(id=1, name="regression", segment_id=1),
            p(id=2, name="profitability", segment_id=2)])
        self.session.commit()
        self.logger.debug('Done generating pipeline type mocks.')

    def _mock_segments(self)-> None:
        self.logger.debug('Generating segment mocks.')
        s = config.Segment
        self.session.add_all([
            s(id=1, name="Patient"),
            s(id=2, name="Payer"),
            s(id=3, name="Distribution")])
        self.session.commit()
        self.logger.debug('Done generating segment mocks.')

    def _mock_transformations(self)-> None:
        self.logger.debug('Generating transformation mocks.')
        t = config.Transformation
        self.session.add_all([
            t(id=1, transformation_template_id=1,
              pipeline_state_id=1, graph_order=0),
            t(id=2, transformation_template_id=1,
              pipeline_state_id=2, graph_order=0),
            t(id=3, transformation_template_id=1,
              pipeline_state_id=2, graph_order=1),
            t(id=9, transformation_template_id=1,
              pipeline_state_id=2, graph_order=0),
            t(id=10, transformation_template_id=1,
              pipeline_state_id=2, graph_order=0),
            t(id=4, transformation_template_id=1,
              pipeline_state_id=4, graph_order=0),
            t(id=5, transformation_template_id=1,
              pipeline_state_id=4, graph_order=0),
            t(id=6, transformation_template_id=1,
              pipeline_state_id=4, graph_order=1),
            t(id=7, transformation_template_id=1,
              pipeline_state_id=4, graph_order=1),
            t(id=8, transformation_template_id=1,
              pipeline_state_id=4, graph_order=2),
            t(id=11, transformation_template_id=1,
              pipeline_state_id=2, graph_order=0),
            t(id=13, transformation_template_id=2,
              pipeline_state_id=2, graph_order=0),
            t(id=12, transformation_template_id=2,
              pipeline_state_id=1, graph_order=1)
        ])
        self.session.commit()
        self.logger.debug('Done generating transformation mocks.')

    def _mock_transformation_templates(self)-> None:
        self.logger.debug('Generating transformation_template mocks.')
        tt = config.TransformationTemplate
        self.session.add_all([
            tt(id=1, name='extract_from_ftp',
                  variable_structures = ''' {"filesystem_path":{"datatype": "string", "description": "the remote path to the files"},
                          "secret_name":{"datatype":"string","description":"the name of the secret in secret manager"},
                          "prefix":{"datatype":"string","description":"the prefix of the files to get on the remote filesystem"},
                          "secret_type_of":{"datatype":"string","description":"the type of the remote server, used in the secret path"}
                          }''',
                          pipeline_state_type_id=1),
            tt(id=2, name='initial_ingest',
                variable_structures = ''' {"delimiter":{"datatype": "string", "description": "the input file delimiter"},
                "skip_rows":{"datatype":"int","description":"the number of rows to skip at the top of the file"},
                "encoding":{"datatype":"string","description":"the encoding of the input file"},
                "input_file_prefix":{"datatype":"string","description":"the prefix of the selected input files"}
                }''',
                pipeline_state_type_id=2)
        ])
        self.session.commit()
        self.logger.debug('Done generating transformation_template mocks.')

    def _mock_transformation_variables(self)->None:
        self.logger.debug('Generating transformation_variables mocks')
        tv = config.TransformationVariable
        self.session.add_all([
            tv(id=5, name='filesystem_path', transformation_id=2, value='banana_stand_data'),
            tv(id=6, name='prefix', transformation_id=2, value='gob'),
            tv(id=1, name='secret_name', transformation_id=2, value='dev-sftp'),
            tv(id=2, name='secret_type_of', transformation_id=2, value='FTP'),

            tv(id=3, name='filesystem_path', transformation_id=3, value='sudden_valley_holdings'),
            tv(id=4, name='secret_name', transformation_id=3, value='dev-sftp'),
            tv(id=12, name='prefix', transformation_id=3, value=''),
            tv(id=11, name='secret_type_of', transformation_id=3, value='FTP'),

            tv(id=7, name='filesystem_path', transformation_id=9, value=''),
            tv(id=8, name='prefix', transformation_id=9, value=''),
            tv(id=9, name='secret_name', transformation_id=9, value='dev-sftp'),
            tv(id=10, name='secret_type_of', transformation_id=9, value='FTP'),

            tv(id=13, name='filesystem_path', transformation_id=1, value='/incoming'),
            tv(id=14, name='prefix', transformation_id=1, value=''),
            tv(id=15, name='secret_name', transformation_id=1, value='dev-sftp'),
            tv(id=16, name='secret_type_of', transformation_id=1, value='FTP'),

            tv(id=17, name='filesystem_path', transformation_id=10, value='/incoming'),
            tv(id=18, name='prefix', transformation_id=10, value='test-extract-root-prefix'),
            tv(id=19, name='secret_name', transformation_id=10, value='dev-sftp'),
            tv(id=20, name='secret_type_of', transformation_id=10, value='FTP'),

            tv(id=21, name='filesystem_path', transformation_id=10, value='/incoming/testing_extract'),
            tv(id=22, name='prefix', transformation_id=11, value=''),
            tv(id=23, name='secret_name', transformation_id=11, value='dev-sftp'),
            tv(id=24, name='secret_type_of', transformation_id=11, value='FTP'),

            tv(id=25, name='delimiter', transformation_id=13, value='|'),
            tv(id=26, name='skip_rows', transformation_id=13, value=1),
            tv(id=27, name='encoding', transformation_id=13, value='iso8859'),
            tv(id=28, name='input_file_prefix', transformation_id=13, value='some-extracted-file')
        ])
        self.session.commit()
        self.logger.debug('Done generating transformation_variables mocks.')

def setup_base_session():
    mock = ConfigurationMocker()
    session = mock.get_session()
    session.add(PharmaceuticalCompany(id=1, display_name='test_client', name='test_client'))
    session.add(Brand(id=1, pharmaceutical_company_id=1, display_name='test_brand', name='test_brand'))
    session.add(Segment(id=1, name='test_segment'))
    session.add(PipelineType(id=1, segment_id=1, name='test_patient_pipeline'))
    session.add(Pipeline(id=1, pipeline_type_id=1, brand_id=1, name='test_pipeline'))
    return session
