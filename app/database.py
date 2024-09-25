from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'postgres://postgres:DessyAdmin@localhost/FASTAPI_DB'
# establishes the postgres conn 
engine = create_engine(SQLALCHEMY_DATABASE_URL)