from __future__ import unicode_literals
from django.db import models
import re, bcrypt

class UserManager(models.Manager):
	def regValidator(self, postData):
		errors = {}
		email_pattern = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
		email_query = self.filter(email=postData['email'])
		if len(postData['first_name']) < 3:
			errors['first_name'] = "First name must be at least 3 characters long."
		if len(postData['last_name']) < 3:
			errors['last_name'] = "Last name must be at least 3 characters long."
		if len(postData['email']) < 2:
			errors['email'] = "Email must be at least 2 characters long."
		elif not email_pattern.match(postData['email']):
			errors['email'] = "Invalid Email."
		elif len(email_query) > 0:
			errors['email'] = "Email is already taken."
		if len(postData['password']) < 3:
			errors['pword_length'] = "Password must be at least 8 characters long."
		if postData['password'] != postData['pwconf']:
			errors['pwconf'] = "Password confirmation must match password."
		return errors
		
	def loginValidator(self, postData):
		user = User.objects.filter(email = postData['login_user_email'])
		errors = {}
		if not user:
			errors['email'] = "Please enter a valid email."
		if user and not bcrypt.checkpw(postData['login_password'].encode(), user[0].password.encode()):
			errors['password'] = "Invalid password."
		return errors

class User(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = UserManager()

class Message(models.Model):
	user = models.ForeignKey(User, related_name='messages')
	#likes = models.ManyToManyField(User, related_name="people_who_like")
	message = models.TextField()
	created_at = models.DateTimeField(auto_now_add = True) 
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()

class Comment(models.Model):
	user = models.ForeignKey(User, related_name='u_comments')
	message = models.ForeignKey(Message, related_name='m_comments')
	#likes = models.ManyToManyField(User, related_name="people_who_like")
	comment = models.TextField()
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()
	