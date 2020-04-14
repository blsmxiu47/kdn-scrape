# -*- coding: utf-8 -*-
# pipelines.py 
from sqlalchemy.orm import sessionmaker
from kdn_articles.models import KdnArticlesDB, db_connect, create_table

# This logging section is optional
import logging

logger = logging.getLogger("kdn_spyder_spider")
logger.setLevel(logging.WARNING)
fh = logging.FileHandler('C:\\Users\\weswa\\python_error_logs\\kdn_articles_spider_log.txt')
fh.setLevel(logging.WARNING)
logger.addHandler(fh)


class KdnArticlesPipeline(object):
	def __init__(self):
		"""
		Initializes database connection and sessionmaker.
		Creates articles table (if not commented out).
		"""
		engine = db_connect()

		# I simply comment this out if I'm just adding to my records 
		#create_table(engine)
		
		self.Session = sessionmaker(bind=engine)

	def process_item(self, item, spider):
		"""
		Save article data in the database.
		"""
		session = self.Session()
		kdndb = KdnArticlesDB()
		kdndb.date_published = item['date_published']
		kdndb.title = item['title']
		kdndb.author = item['author']
		kdndb.author_info = item['author_info']
		kdndb.tags = item['tags']
		kdndb.excerpt = item['excerpt']
		kdndb.post_text = item['post_text']
		kdndb.url = item['url']


		try:
			session.add(kdndb)
			session.commit()
		# Optional:
		except UnicodeEncodeError as e:
			logger.debug(e, exc_info=False)
			raise
		
		except:
			session.rollback()
			raise
		finally:
			session.close()
			
		return item