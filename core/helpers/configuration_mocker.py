from sqlalchemy import create_engine
import core.models.configuration as config
import logging

class ConfigurationMocker:
    ''' for development, creates in-memory database instance and a matching session.
        optionally gives you a bunch of mocked data.
    '''

    def __init__(self):
        engine = create_engine('sqlite:///:memory:')

        # this instansiates the in-memory sqlite instance
        config.Base.metadata.create_all(engine)

        session = config.Session(engine)
        self.session = session.get_session()

    def get_session(self):
        return self.session

    def generate_mocks(self):
        self._mock_transformation_templates()
        self._mock_transformations()
        self._mock_extract_configurations()

    def _mock_transformations(self):
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

    def _mock_extract_configurations(self):
        logging.debug('Generating extract_configuation mocks...')
        ex = config.ExtractConfiguration
        self.session.add_all([
            ex(id=1, transformation_id=2, filesystem_path='', prefix='',secret_name='bluth'),
            ex(id=2, transformation_id=2, filesystem_path='banana_stand', prefix='gob',secret_name='bluth'),
            ex(id=3, transformation_id=3, filesystem_path='sudden_valley', prefix='',secret_name='bluth'),
            ex(id=4, transformation_id=1, filesystem_path='', prefix='',secret_name='sitwell'),
            ex(id=5, transformation_id=1, filesystem_path='', prefix='001545',secret_name='sitwell'),
            ex(id=6, transformation_id=1, filesystem_path='200-1', prefix='',secret_name='sitwell')
            ])
        self.session.commit()
        logging.debug('Done generating extract_configuration mocks.')

    def _mock_transformation_templates(self):
        logging.debug('Generating transformation_template mocks...')
        tt = config.TransformationTemplate
        self.session.add_all([
            tt(id=1, name='always_money_in_the_banana_stand'),
            tt(id=2, name='02_finish_each_others_sandwiches')
        ])
        self.session.commit()
        logging.debug('Done generating transformation_template mocks.')

