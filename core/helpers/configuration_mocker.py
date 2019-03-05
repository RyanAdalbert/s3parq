from sqlalchemy.orm.session import Session
from sqlalchemy import create_engine
import core.models.configuration as config
from core.logging import LoggerMixin


class ConfigurationMocker(LoggerMixin):
    ''' for development, creates in-memory database instance and a matching session.
        optionally gives you a bunch of mocked data.
    '''

    def __init__(self)-> None:
        engine = config.GenerateEngine().get_engine()

        # this instansiates the in-memory sqlite instance
        config.Base.metadata.create_all(engine)

        session = config.Session(engine)
        self.session = session.get_session()

    def get_session(self) -> Session:
        return self.session

    def generate_mocks(self)-> None:
        self._mock_pharmaceutical_companies()
        self._mock_brands()
        self._mock_segments()
        self._mock_pipeline_types()
        self._mock_pipelines()
        self._mock_pipeline_state_types()
        self._mock_pipeline_states()
        self._mock_transformation_templates()
        self._mock_transformations()
        self._mock_extract_configurations()
        self._mock_initial_ingest_configurations()

    def _mock_brands(self)-> None:
        self.logger.debug('Generating brand mocks.')
        b = config.Brand
        self.session.add_all([
            b(id=1, name="Teamocil", display_name="Teamocil",
              pharmaceutical_company_id=1),
            b(id=2, name="Cornballer2", display_name="Corn Baller", pharmaceutical_company_id=2)])
        self.session.commit()
        self.logger.debug('Done generating brand mocks.')


    def _mock_initial_ingest_configurations(self)-> None:
        self.logger.debug('Generating initial_ingest mocks.')
        ii = config.InitialIngestConfiguration
        self.session.add_all([
            ii(id=1, transformation_id=11, delimiter=',', skip_rows=0, encoding="utf-8")
        ])
        self.session.commit()
        self.logger.debug('Done generating initial_ingest mocks.')


    def _mock_extract_configurations(self)-> None:
        self.logger.debug('Generating extract_configuation mocks.')
        ex = config.ExtractConfiguration
        self.session.add_all([
            ex(id=1, transformation_id=2, filesystem_path='',
               prefix='', secret_name='dev-sftp', secret_type_of='FTP'),
            ex(id=2, transformation_id=2, filesystem_path='banana_stand_data',
               prefix='gob', secret_name='dev-sftp', secret_type_of='FTP'),
            ex(id=3, transformation_id=3, filesystem_path='sudden_valley_holdings',
               prefix='', secret_name='dev-sftp', secret_type_of='FTP'),
            ex(id=4, transformation_id=1, filesystem_path='/incoming',
               prefix='', secret_name='dev-sftp', secret_type_of='FTP'),
            ex(id=5, transformation_id=1, filesystem_path='/incoming',
               prefix='test-extract-root-prefix', secret_name='dev-sftp', secret_type_of='FTP'),
            ex(id=6, transformation_id=1, filesystem_path='/incoming/testing_extract',
               prefix='', secret_name='dev-sftp', secret_type_of='FTP')
        ])
        self.session.commit()
        self.logger.debug('Done generating extract_configuration mocks.')

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
            p(id=1, name="Raw"),
            p(id=2, name="Ingest"),
            p(id=3, name="Master"),
            p(id=4, name="Enhance"),
            p(id=5, name="Enrich"),
            p(id=6, name="Metrics"),
            p(id=7, name="Dimensional")])
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
            t(id=3, transformation_template_id=2,
              pipeline_state_id=2, graph_order=1),
            t(id=9, transformation_template_id=2,
              pipeline_state_id=2, graph_order=0),
            t(id=10, transformation_template_id=2,
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
            t(id=11, transformation_template_id=3,
              pipeline_state_id=2, graph_order=0)
        ])
        self.session.commit()
        self.logger.debug('Done generating transformation mocks.')

    def _mock_transformation_templates(self)-> None:
        self.logger.debug('Generating transformation_template mocks.')
        tt = config.TransformationTemplate
        self.session.add_all([
            tt(id=1, name='always_money_in_the_banana_stand'),
            tt(id=2, name='02_finish_each_others_sandwiches'),
            tt(id=3, name='shared_initial_ingest')
        ])
        self.session.commit()
        self.logger.debug('Done generating transformation_template mocks.')
