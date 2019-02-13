from sqlalchemy import engine, create_engine, Column, Integer, String, Boolean, TIMESTAMP, text, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import session, sessionmaker, relationship
from core.constants import DEV_CONFIGURATION_APPLICATION_CONN_STRING, ENVIRONMENT
from core.secret import Secret
Base = declarative_base()


class Session():
    ''' INTENT: Builds and returns a database session.
        ARGS:
        RETURNS instance of sqlalchemy.orm.session.Session https://docs.sqlalchemy.org/en/rel_1_2/orm/tutorial.html#creating-a-session
    '''

    def __init__(self, engine: engine.base.Engine) -> None:
        s = sessionmaker(bind=engine)
        self.session = s()

    def get_session(self) -> session.Session:
        return self.session

class GenerateEngine:
    """ abstract defining connections here. Local assumes a psql instance in a local docker container. """

    def __init__(self, in_memory:bool=True) -> None:
        """ So the default development configuration database is an in-memory sqlite instance. 
            This is fast and easy and atomic (resets after every execution) but it is NOT exactly the same as 
            the prod PG instance. When we want an identical configuration environment, setting in_memory to False 
            gives you the local docker container PG. """

        if ENVIRONMENT == "dev":
            if in_memory:
                self._url = "sqlite://"
            else:
                self._url = DEV_CONFIGURATION_APPLICATION_CONN_STRING
        else:
            self._url = self._secret_defined_url()

    @property
    def url(self) -> str: 
        return self._url

    def get_engine(self) -> engine.base.Engine:
        engine = create_engine(self._url)
        return engine

    def _secret_defined_url(self) -> str:
        """ creates a session connecting to the correct configuration_application db based on ENV."""
        secret = Secret(env=ENVIRONMENT, 
                        name='configuration_application',
                        type_of='database',
                        mode='read'
                        )
        if secret.rdbms == "postgres":
            conn_string = f"postgresql://{secret.user}:{secret.password}@{host}/{database}"
        else:
            m = "Only postgres databases are supported for configuration_application at this time."
            logger.critical(m)
            raise NotImplementedError(m)
        return conn_string


"""Mixins
    Inheritance classes to supply standardized columns.
"""


class UniversalMixin:
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=func.now())
    last_actor = Column(String)


class UniversalWithPrimary(UniversalMixin):
    id = Column(Integer, primary_key=True)


"""ORM classes
   
Each of these classes represents an entity in the database.
Logic for updates and audits will be handled via migrations. 
"""


class Brand(UniversalWithPrimary, Base):
    __tablename__ = 'brands'
    name = Column(String, nullable=False)
    display_name = Column(String, nullable=False)
    pharmaceutical_company_id = Column(Integer, ForeignKey(
        'pharmaceutical_companies.id'), nullable=False)
    pharmaceutical_company = relationship(
        "PharmaceuticalCompany", back_populates='brands')
    pipelines = relationship("Pipeline", back_populates='brand')


class ExtractConfiguration(UniversalWithPrimary, Base):
    __tablename__ = 'extract_configurations'
    transformation_id = Column(Integer, ForeignKey(
        'transformations.id'), nullable=False)
    filesystem_path = Column(String)
    prefix = Column(String)
    secret_type_of = Column(String, nullable=False)
    secret_name = Column(String, nullable=False)
    transformation = relationship(
        "Transformation", back_populates='extract_configurations')


class PharmaceuticalCompany(UniversalWithPrimary, Base):
    __tablename__ = 'pharmaceutical_companies'
    name = Column(String, nullable=False)
    display_name = Column(String, nullable=False)
    brands = relationship("Brand", back_populates='pharmaceutical_company')


class Pipeline(UniversalWithPrimary, Base):
    __tablename__ = 'pipelines'
    name = Column(String, nullable=False)
    pipeline_type_id = Column(Integer, ForeignKey(
        'pipeline_types.id'), nullable=False)
    pipeline_type = relationship("PipelineType")
    is_active = Column(Boolean, nullable=False, default= True)
    brand_id = Column(Integer, ForeignKey('brands.id'), nullable=False)
    brand = relationship("Brand", back_populates="pipelines")
    run_frequency = Column(String)
    pipeline_states = relationship("PipelineState", back_populates='pipeline')


class PipelineState(UniversalWithPrimary, Base):
    __tablename__ = 'pipeline_states'
    pipeline_state_type_id = Column(Integer, ForeignKey(
        'pipeline_state_types.id'), nullable=False)
    pipeline_state_type = relationship("PipelineStateType")
    pipeline_id = Column(Integer, ForeignKey('pipelines.id'), nullable=False)
    pipeline = relationship("Pipeline", back_populates="pipeline_states")
    graph_order = Column(Integer, nullable=False)
    transformations = relationship("Transformation")

class PipelineStateType(UniversalWithPrimary, Base):
    __tablename__ = 'pipeline_state_types'
    name = Column(String, nullable=False)


class PipelineType(UniversalWithPrimary, Base):
    __tablename__ = 'pipeline_types'
    name = Column(String, nullable=False)
    segment_id = Column(Integer, ForeignKey('segments.id'), nullable=False)
    segment = relationship("Segment", back_populates='pipeline_types')


class Segment(UniversalWithPrimary, Base):
    __tablename__ = 'segments'
    name = Column(String, nullable=False)
    pipeline_types = relationship("PipelineType", back_populates='segment')


class Transformation(UniversalWithPrimary, Base):
    __tablename__ = 'transformations'
    transformation_template_id = Column(Integer,  ForeignKey(
        'transformation_templates.id'), nullable=False)
    transformation_template = relationship("TransformationTemplate")
    pipeline_state_id = Column(Integer,  ForeignKey(
        'pipeline_states.id'), nullable=False)
    pipeline_state = relationship("PipelineState", back_populates='transformations')
    graph_order = Column(Integer, nullable=False, server_default=text('0'))
    extract_configurations = relationship(
        "ExtractConfiguration", order_by=ExtractConfiguration.id, back_populates='transformation')


class TransformationTemplate(UniversalWithPrimary, Base):
    __tablename__ = 'transformation_templates'
    name = Column(String, nullable=False)
