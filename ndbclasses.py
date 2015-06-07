from google.appengine.ext import ndb
import os
import jinja2
from collections import namedtuple

#Constants for this Stage 
DEFAULT_NOTES = 'Notes'
DEFAULT_COMMENTS = 'Comments'
#Constants for this Stage 
TITLE = 'Stage5'
SUBTITLE = '"Allow Comments on your Page"'
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), 'jinja2_templates')
JINJA_ENVIRONMENT = jinja2.Environment(loader = jinja2.FileSystemLoader(TEMPLATES_DIR),autoescape = True)
ARTICLE = namedtuple('Article', ['header','subheader','note','noteid','comments'])
ADDEDARTICLE = namedtuple('Article', ['header','subheader','note','noteid'])
COMMENT = namedtuple('Comment', ['commentednote','commentauthor','commenttext'])


def note_key(note_name=DEFAULT_NOTES):
	"""Constructs a Datastore key for a Note entity.

	We use note_name as the key.
	"""
	return ndb.Key('Note', note_name)

def comment_key(comment_name=DEFAULT_COMMENTS):
	"""Constructs a Datastore key for a Comment entity.

	We use comment_name as the key.
	"""
	return ndb.Key('Comment', comment_name)

	
class Author(ndb.Model):
	"""ndb Model for an author."""
	userid = ndb.StringProperty(indexed=True)
	name = ndb.StringProperty(indexed=False)
	email = ndb.StringProperty(indexed=False)

class Comment(ndb.Model):
	commentauthor = ndb.StructuredProperty(Author)
	commenttext = ndb.StringProperty(indexed=True)
	commentednote = ndb.IntegerProperty(indexed=True)
	commentcreatedtimestamp = ndb.DateTimeProperty(auto_now_add=True)
	
	# get all comments related to an article
	@classmethod
	def get_all(self,noteid):
		""" get all comments"""
		# Using Ancestor Queries, because of their strong consistensy
		comment_name = DEFAULT_COMMENTS
		all_comments_query = self.query(ancestor = comment_key(comment_name),
							 filters=ndb.AND(self.commentednote == noteid)).order(self.commentcreatedtimestamp)
		all_comments = all_comments_query.fetch()
		return all_comments
	
class Article(ndb.Model):
	""" ndb Model for an Article """
	note = ndb.TextProperty(indexed=False)
	noteid = ndb.IntegerProperty(indexed=True)
	header = ndb.StringProperty(indexed=True)
	subheader = ndb.StringProperty(indexed=False)
	
	#get all articles
	@classmethod
	def get_all(self):
		""" get all Articles"""
		# Using Ancestor Queries, because of their strong consistensy
		note_name = DEFAULT_NOTES
		all_notes_query = self.query(ancestor = note_key(note_name)).order(self.noteid)
		all_notes = all_notes_query.fetch()
		return all_notes 
	
	# get single article 
	@classmethod	
	def get_single(self,noteid):
		""" get single Article"""
		# Using Ancestor Queries, because of their strong consistensy
		note_name = DEFAULT_NOTES
		single_note_query = self.query(ancestor = note_key(note_name),
							filters=(self.noteid == noteid))
		single_note = single_note_query.fetch(1)
		return single_note 
	
	
	