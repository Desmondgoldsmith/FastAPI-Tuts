from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'postgres://postgres:DessyAdmin@127.0.0.1:8000/localhost/FASTAPI_DB'