from sqlalchemy import create_engine, Column, Integer, String, BOOLEAN, TIMESTAMP, text, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship 

#engine = create_engine("postgresql+psycopg2://user:password@/dbname")


Base = declarative_base()

class Session():
    ''' Builds and returns a database session.
        Accepts an engine from the create_engine method
    '''

    def __init__(self, engine):
        s = sessionmaker(bind=engine)
        self.session = s

    def get_session(self):
        return self.session

class ExtractConfiguration(Base):
    __tablename__ = 'extract_configurations'

    id = Column(Integer, primary_key = True)
    transformation_id = Column(Integer, ForeignKey('transformations.id'),nullable = False )
    filesystem_path = Column(String)
    prefix = Column(String)
    secret_name = Column(String, nullable = False)
    is_deleted = Column(BOOLEAN, nullable = False, server_default = '0')
    created_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default = func.now())
    updated_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default = func.now()) # let's add a trigger to this on the PG side instead of having the application drive it
    last_actor = Column(String)
    transformation = relationship("Transformation")
    
class Transformation(Base):
##TODO: temporarily removed the referential constraints to get DC-18 unblocked
    __tablename__ = 'transformations'
    id = Column(Integer, primary_key = True)
    #transformation_template_id = Column(Integer,  ForeignKey('transformation_templates.id'), nullable = False)
    transformation_template_id = Column(Integer) 
    #pipeline_state_id = Column(Integer,  ForeignKey('pipeline_states.id'), nullable = False)  
    pipeline_state_id = Column(Integer)
    graph_order = Column(Integer, nullable = False, server_default = text('0'))
    is_deleted = Column(BOOLEAN, nullable = False, server_default = '0')
    created_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default = func.now())
    updated_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default = func.now()) # let's add a trigger to this on the PG side instead of having the application drive it
    last_actor = Column(String)
    extract_configurations = relationship("ExtractConfiguration", order_by = ExtractConfiguration.id, back_populates = 'transformation')

class TransformationTemplate(Base):
    __tablename__ = 'transformation_templates'
    id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False)
    is_deleted = Column(BOOLEAN) #, nullable = False, server_default = '0')
    created_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default = func.now())
    updated_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default = func.now()) # let's add a trigger to this on the PG side instead of having the application drive it
    last_actor = Column(String)


def _dev_in_memory():
    ''' For development, creates in-memory instance and returns a loaded session '''
    
    engine = create_engine('sqlite:///:memory:')

    ## build all
    Base.metadata.create_all(engine)

    ## create and return session
    session = Session(engine)
    return session.session()


