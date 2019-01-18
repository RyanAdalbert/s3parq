from sqlalchemy import create_engine, Column, Integer, String, BOOLEAN, TIMESTAMP, text, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

#engine = create_engine("postgresql+psycopg2://user:password@/dbname")

Base = declarative_base()


class Session():
    ''' INTENT: Builds and returns a database session.
        ARGS:
            - engine (obj): requires an instance of sqlachemy.engine.base.Engine https://docs.sqlalchemy.org/en/rel_1_2/core/engines.html
        RETURNS instance of sqlalchemy.orm.session.Session https://docs.sqlalchemy.org/en/rel_1_2/orm/tutorial.html#creating-a-session
    '''

    def __init__(self, engine):
        s = sessionmaker(bind=engine)
        self.session = s()

    def get_session(self):
        return self.session


"""ORM classes
   
Each of these classes represents an entity in the database.
Logic for updates and audits will be handled via migrations. 
"""


class ExtractConfiguration(Base):
    __tablename__ = 'extract_configurations'

    id = Column(Integer, primary_key=True)
    transformation_id = Column(Integer, ForeignKey(
        'transformations.id'), nullable=False)
    filesystem_path = Column(String)
    prefix = Column(String)
    secret_name = Column(String, nullable=False)
    is_deleted = Column(BOOLEAN, nullable=False, server_default='0')
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=func.now())
    # let's add a trigger to this on the PG side instead of having the application drive it
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=func.now())
    last_actor = Column(String)
    transformation = relationship("Transformation")


class Transformation(Base):
    # TODO: temporarily removed the referential constraints to get DC-18 unblocked
    __tablename__ = 'transformations'
    id = Column(Integer, primary_key=True)
    #transformation_template_id = Column(Integer,  ForeignKey('transformation_templates.id'), nullable = False)
    transformation_template_id = Column(Integer)
    #pipeline_state_id = Column(Integer,  ForeignKey('pipeline_states.id'), nullable = False)
    pipeline_state_id = Column(Integer)
    graph_order = Column(Integer, nullable=False, server_default=text('0'))
    is_deleted = Column(BOOLEAN, nullable=False, server_default='0')
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=func.now())
    # let's add a trigger to this on the PG side instead of having the application drive it
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=func.now())
    last_actor = Column(String)
    extract_configurations = relationship(
        "ExtractConfiguration", order_by=ExtractConfiguration.id, back_populates='transformation')


class TransformationTemplate(Base):
    __tablename__ = 'transformation_templates'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    is_deleted = Column(BOOLEAN)  # , nullable = False, server_default = '0')
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=func.now())
    # let's add a trigger to this on the PG side instead of having the application drive it
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=func.now())
    last_actor = Column(String)



