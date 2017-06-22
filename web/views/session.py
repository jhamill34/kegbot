import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

engine_string = os.environ.get('SQL_STRING')
engine = create_engine(engine_string)

Base.metadata.create_all(engine)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
