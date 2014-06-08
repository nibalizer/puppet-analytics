from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import settings

Base = declarative_base()
engine = create_engine(settings.sqlite_db, echo=True)
Session = sessionmaker(bind=engine)
