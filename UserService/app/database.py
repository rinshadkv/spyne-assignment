import logging

from sqlalchemy import create_engine
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
