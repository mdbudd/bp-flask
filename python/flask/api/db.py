from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy import Boolean, Column, Float, String, Integer, MetaData, Table
from config import DATABASE_URL

db = SQLAlchemy()
# engine = create_engine(DATABASE_URL, pool_size=20, max_overflow=0)
engine = create_engine("sqlite:///database.db")

tableMeta = MetaData("sqlite:///database.db")

# VP_META_PAGES = Table("VP_META_PAGES", tableMeta, autoload=True)
# DS_EMPLOYEE = Table("DS_EMPLOYEE", tableMeta, autoload=True, schema="HIR_OWNER")

Session = sessionmaker(bind=engine)
Base = declarative_base()
session = Session()
