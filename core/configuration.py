from sqlalchemy import create_engine, Column, Integer, String, BOOLEAN, TIMESTAMP, text, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship 

#engine = create_engine("postgresql+psycopg2://user:password@/dbname")


Base = declarative_base()

class Session():
    
    def __init__(self, engine):
        self.session = sessionmaker(bind=engine)

    def get_session(self):
        return self.session()

class ExtractConfiguration(Base):
    __tablename__ = 'extract_configurations'

    id = Column(Integer, primary_key = True)
    transformation_id = Column(Integer, ForeignKey('transformations.id'),nullable = False )
    filesystem_path = Column(String, nullable = False)
    prefix = Column(String, nullable = False)
    secret_name = Column(String, nullable = False)
    is_deleted = Column(BOOLEAN, nullable = False, server_default = 'f')
    created_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default = func.now())
    updated_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default = func.now()) # let's add a trigger to this on the PG side instead of having the application drive it
    last_actor = Column(String)
    parent = relationship 
    parent = relationship('Transformation')
    
class Transformation(Base):
    __tablename__ = 'transformations'
    id = Column(Integer, primary_key = True)
    transformation_template_id = Column(Integer,  ForeignKey('transformation_templates.id'), nullable = False)
    pipeline_state_id = Column(Integer)
    #pipeline_state_id = Column(Integer,  ForeignKey('pipeline_states.id'), nullable = False)
    graph_order = Column(Integer, nullable = False, server_default = text('0'))
    is_deleted = Column(BOOLEAN, nullable = False, server_default = 'f')
    created_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default = func.now())
    updated_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default = func.now()) # let's add a trigger to this on the PG side instead of having the application drive it
    last_actor = Column(String)
    children = relationship("ExtractConfiguration")

class TransformationTemplate(Base):
    __tablename__ = 'transformation_templates'
    id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False)
    is_deleted = Column(BOOLEAN) #, nullable = False, server_default = 'f')
    created_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default = func.now())
    updated_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default = func.now()) # let's add a trigger to this on the PG side instead of having the application drive it
    last_actor = Column(String)
    children = relationship("Transformation")


def dev_in_memory():
    ''' For development, creates in-memory instance and returns a loaded session '''
    
    engine = create_engine('sqlite:///:memory:')

    ## build all
    Base.metadata.create_all(engine)

    ## create and return session
    session = Session(engine)
    return session
