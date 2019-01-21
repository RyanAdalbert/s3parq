from sqlalchemy.orm.session import Session
from sqlalchemy import create_engine
import core.models.configuration as config
import logging


class ConfigurationMocker:
    ''' for development, creates in-memory database instance and a matching session.
        optionally gives you a bunch of mocked data.
    '''

    def __init__(self)-> None:
        # TODO: migrate to local postgres instance
        engine = create_engine('sqlite://')
        #engine = config.GenEngine(env='dev', local=True).get_engine()

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

    def _mock_brands(self)-> None:
        logging.debug('Generating brand mocks...')
        b = config.Brand
        self.session.add_all([
            b(id=1, name="Teamocil", display_name="Teamocil",
              pharmaceutical_company_id=1),
            b(id=2, name="Cornballer", display_name="Corn Baller", pharmaceutical_company_id=2)])
        self.session.commit()
        logging.debug('Done generating brand mocks.')

    def _mock_extract_configurations(self)-> None:
        logging.debug('Generating extract_configuation mocks...')
        ex = config.ExtractConfiguration
        self.session.add_all([
            ex(id=1, transformation_id=2, filesystem_path='',
               prefix='', secret_name='bluth'),
            ex(id=2, transformation_id=2, filesystem_path='banana_stand_data',
               prefix='gob', secret_name='bluth'),
            ex(id=3, transformation_id=3, filesystem_path='sudden_valley_holdings',
               prefix='', secret_name='bluth'),
            ex(id=4, transformation_id=1, filesystem_path='',
               prefix='', secret_name='sitwell'),
            ex(id=5, transformation_id=1, filesystem_path='',
               prefix='001545', secret_name='sitwell'),
            ex(id=6, transformation_id=1, filesystem_path='200-1',
               prefix='', secret_name='sitwell')
        ])
        self.session.commit()
        logging.debug('Done generating extract_configuration mocks.')

    def _mock_pharmaceutical_companies(self)-> None:
        logging.debug('Generating pharmaceutical company mocks...')
        p = config.PharmaceuticalCompany
        self.session.add_all([
            p(id=1, display_name="Natural Life Food Company", name='Nfoods'),
            p(id=2, display_name="Sitwell Home Construction", name="Sitwell")])
        self.session.commit()
        logging.debug('Done generating pharmaceutical company mocks.')

    def _mock_pipelines(self)-> None:
        logging.debug('Generating pipeline mocks...')
        p = config.Pipeline
        self.session.add_all([
            p(id=1, name="bluth_banana_regression", brand_id=2,
              pipeline_type_id=1, run_frequency='daily'),
            p(id=2, name="bluth_profitability", brand_id=2,
              pipeline_type_id=2, run_frequency='hourly'),
            p(id=3, name="temocil_profitablility", brand_id=1, pipeline_type_id=1, run_frequency='daily')])
        self.session.commit()
        logging.debug('Done generating pipeline mocks.')

    def _mock_pipeline_states(self)-> None:
        logging.debug('Generating pipeline state mocks...')
        p = config.PipelineState
        self.session.add_all([
            p(id=1, pipeline_state_type_id=1, pipeline_id=1, graph_order=0),
            p(id=2, pipeline_state_type_id=2, pipeline_id=1, graph_order=1),
            p(id=3, pipeline_state_type_id=3, pipeline_id=1, graph_order=2),
            p(id=4, pipeline_state_type_id=1, pipeline_id=2, graph_order=0)])
        self.session.commit()
        logging.debug('Done generating pipeline state mocks.')

    def _mock_pipeline_state_types(self)-> None:
        logging.debug('Generating pipeline state type mocks...')
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
        logging.debug('Done generating pipeline state type mocks.')

    def _mock_pipeline_types(self)-> None:
        logging.debug('Generating pipeline type mocks...')
        p = config.PipelineType
        self.session.add_all([
            p(id=1, name="regression", segment_id=1),
            p(id=2, name="profitability", segment_id=2)])
        self.session.commit()
        logging.debug('Done generating pipeline type mocks.')

    def _mock_segments(self)-> None:
        logging.debug('Generating segment mocks...')
        s = config.Segment
        self.session.add_all([
            s(id=1, name="Patient"),
            s(id=2, name="Payer"),
            s(id=3, name="Distribution")])
        self.session.commit()
        logging.debug('Done generating segment mocks.')

    def _mock_transformations(self)-> None:
        logging.debug('Generating transformation mocks...')
        t = config.Transformation
        self.session.add_all([
            t(id=1, transformation_template_id=1,
              pipeline_state_id=1, graph_order=0),
            t(id=2, transformation_template_id=1,
              pipeline_state_id=2, graph_order=0),
            t(id=3, transformation_template_id=2,
              pipeline_state_id=2, graph_order=1)
        ])
        self.session.commit()
        logging.debug('Done generating transformation mocks.')

    def _mock_transformation_templates(self)-> None:
        logging.debug('Generating transformation_template mocks...')
        tt = config.TransformationTemplate
        self.session.add_all([
            tt(id=1, name='always_money_in_the_banana_stand'),
            tt(id=2, name='02_finish_each_others_sandwiches')
        ])
        self.session.commit()
        logging.debug('Done generating transformation_template mocks.')
