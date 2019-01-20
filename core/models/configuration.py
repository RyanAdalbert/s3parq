from sqlalchemy import engine, create_engine, Column, Integer, String, BOOLEAN, TIMESTAMP, text, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()


class Session():
    ''' INTENT: Builds and returns a database session.
        ARGS:
        RETURNS instance of sqlalchemy.orm.session.Session https://docs.sqlalchemy.org/en/rel_1_2/orm/tutorial.html#creating-a-session
    '''

    def __init__(self, engine: engine.base.Engine) -> None:
        s = sessionmaker(bind=engine)
        self.session = s()

    def get_session(self):
        return self.session

class GenEngine:
    """ abstract defining connections here. Local assumes a psql instance on the metal. """     
    def __init__(self, env: str, local: bool = False ) -> None:
        if local:
            self.engine = self._local_engine()
        else:
            self.engine = self._secret_defined_engine()

    def get_engine(self) -> engine.base.Engine:
        return self.engine

    def _local_engine(self) -> engine.base.Engine:
            return create_engine('postgresql://configurator:configurator@localhost/configuration_application')

    def _secret_defined_engine(self) -> engine.base.Engine:
            ##TODO: in DC-57 update this to use secret
            pass
   
    

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


class ExtractConfiguration(UniversalWithPrimary, Base):
    __tablename__ = 'extract_configurations'
    transformation_id = Column(Integer, ForeignKey(
        'transformations.id'), nullable=False)
    filesystem_path = Column(String)
    prefix = Column(String)
    secret_name = Column(String, nullable=False)
    transformation = relationship("Transformation")


class Transformation(UniversalWithPrimary, Base):
    # TODO: temporarily removed the referential constraints to get DC-18 unblocked
    __tablename__ = 'transformations'
    #transformation_template_id = Column(Integer,  ForeignKey('transformation_templates.id'), nullable = False)
    transformation_template_id = Column(Integer)
    #pipeline_state_id = Column(Integer,  ForeignKey('pipeline_states.id'), nullable = False)
    pipeline_state_id = Column(Integer)
    graph_order = Column(Integer, nullable=False, server_default=text('0'))
    extract_configurations = relationship(
        "ExtractConfiguration", order_by=ExtractConfiguration.id, back_populates='transformation')


class TransformationTemplate(UniversalWithPrimary, Base):
    __tablename__ = 'transformation_templates'
    name = Column(String, nullable=False)
    is_deleted = Column(BOOLEAN)  # , nullable = False, server_default = '0')
