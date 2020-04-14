# models.py
from sqlalchemy import create_engine, MetaData, Column, Integer, String, Date, Text
from sqlalchemy.ext.declarative import declarative_base

from scrapy.utils.project import get_project_settings

import logging

DeclarativeBase = declarative_base()

def db_connect():
	# DB connection using settings from (above) settings.py
	# UTF-8 generally the safest encoding to work with, but still occasionally have to troubleshoot
	return create_engine(get_project_settings().get("CONNECTION_STRING"), encoding='utf-8')

def create_table(engine):
	table_name = 'kdn_articles'
	metadata = MetaData(engine, reflect=True)
	table = metadata.tables.get(table_name)

	# If kdn_articles table exists in db, then delete and start from scratch
	if table is not None:
		logging.info(f'deleting {table_name} table')
		DeclarativeBase.metadata.drop_all(engine, [table], checkfirst=True)
	DeclarativeBase.metadata.create_all(engine)

class KdnArticlesDB(DeclarativeBase):
	__tablename__ = "kdn_articles"
	
	# sqlalchemy syntax for defining columns in a DB. 
	#  Note the additional id primary key, not from our item fields
	id = Column(Integer, primary_key=True)
	title = Column('title', Text(), unique=True)
	date_published = Column('date_published', Date())
	author = Column('author', String(128))
	author_info = Column('author_info', String(256))
	tags = Column('description', String(256))
	excerpt = Column('excerpt', Text())
	post_text = Column('post_text', Text())
	url = Column('url', Text())
