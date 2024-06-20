import logging

from sqlalchemy import create_engine,MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# PostgreSQL database connection details
user = 'user'
password = 'password'
host = 'postgres'
port = '5432'
databaseName = 'spyne'

SQLALCHEMY_DATABASE_URL = f'postgresql://{user}:{password}@{host}:{port}/{databaseName}'

# Create a SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata = MetaData()

# Reflect existing tables into metadata
metadata.reflect(bind=engine, extend_existing=True)

# Define declarative base with reflected metadata
Base = declarative_base(metadata=metadata)