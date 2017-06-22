from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

engine_string = 'postgresql://docker:mysecretpassword@db:5432/kegbot'
engine = create_engine(engine_string)

Base.metadata.create_all(engine)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
