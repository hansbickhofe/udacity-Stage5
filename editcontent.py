#!/usr/bin/env python
# -*- coding: utf-8 -*-
import webapp2
import cgi
import logging

from google.appengine.api import users
from ndbclasses import *
from google.appengine.ext import ndb


def note_key(note_name=DEFAULT_NOTES):
	"""Constructs a Datastore key for a Note entity.

	We use note_name as the key.
	"""
	return ndb.Key('Note', note_name)
	
# using Handler from Videolesson		
class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a,**kw)
	
	def render_str(self, template, **params):
		t = JINJA_ENVIRONMENT.get_template(template)
		return t.render(params)
	
	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class EditContentHandler(Handler):
	def get(self):
		# No get allowed
		self.redirect("/")		
		
	def post(self):
		user = users.get_current_user()
		# Check if User is logged in and admin
		if users.is_current_user_admin():
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'
			user_mail = user.email()
			user_nickname = user.nickname()
			user_userid = user.user_id()
			# If this an edit request, get Article by noteid
			if cgi.escape(self.request.get("edit")) == "1":
				note_to_edit = int(cgi.escape(self.request.get("note_id")))
				note = Article.get_single(note_to_edit)
				logging.info(str(note))
				#Render Article entity into contenform
				self.render('contentform.html', pagetitle = TITLE, pagesubtitle = SUBTITLE, editnote = note, user = user_userid, loginurl = url, linktext = url_linktext)
			
			elif cgi.escape(self.request.get("del")) == "1":
				note_to_delete = int(cgi.escape(self.request.get("note_id")))
				# Using Ancestor Queries, because of their strong consistensy
				note_name = DEFAULT_NOTES
				# Query for entity Key
				articlequery = Article.query(ancestor=note_key(note_name),
											filters=(Article.noteid == note_to_delete)).fetch(1,keys_only=True)
				# Get entity and update Article
				article = articlequery[0].delete()
				self.redirect("/")	
			else:
				#If no edit, we save the content
				header = cgi.escape(self.request.get("header"))
				subheader = cgi.escape(self.request.get("subheader"))
				note = self.request.get("note")
				noteid = int(cgi.escape(self.request.get("noteindex")))
				# Using Ancestor Queries, because of their strong consistensy
				note_name = DEFAULT_NOTES
				# Query for entity Key
				articlequery = Article.query(ancestor=note_key(note_name),
											filters=(Article.noteid == noteid)).fetch(1,keys_only=True)
				# Get entity and update Article
				article = articlequery[0].get()				
				article.header = header
				article.subheader = subheader
				article.noteid = noteid
				article.note = note
				# Put entity into Datastore
				article.put()
				# Redirect to Frontpag
				self.redirect("/")							
		else:
			self.redirect("/")							
	
app = webapp2.WSGIApplication([
	('/editcontent', EditContentHandler),
], debug=True)		