from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt


def index(request):
	if 'logged_in' not in request.session:
		return render(request, 'wall/index.html')
	else:
		return redirect('/success')

def register(request):
	errors = User.objects.regValidator(request.POST)
	if len(errors) > 0:
		for k,v in errors.items():
		 	messages.error(request, v)
	else:
		hashpw1 = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
		User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'],email = request.POST['email'], password=hashpw1)
		user = User.objects.last()
		request.session['logged_in'] = user.id
		return redirect('/success')

	return redirect('/')

def login(request):
	errors = User.objects.loginValidator(request.POST)
	if len(errors) > 0:
		for k,v in errors.items():
		 	messages.error(request, v)
	else:
		user = User.objects.get(email=request.POST['login_user_email'])
		request.session['logged_in'] = user.id
		return redirect('/success')
	
	return redirect('/')

def logout(request):
	request.session.clear()
	return redirect('/')

def success(request):
	context = {
	'user': User.objects.get(id=request.session['logged_in']),
	'post_data':Message.objects.all(),
	'comment_data':Comment.objects.all(),
	}
	
	return render(request, 'wall/wall.html',context)

def add_message(request):
	Message.objects.create(message=request.POST['add_message'], user=User.objects.get(id=request.session['logged_in']))
	#messages.success(request,'Message postd successfully.')
	return redirect('/success')

def delete_message(request,id):
	m = Message.objects.get(id=id)
	m.delete()
	return redirect('/success') 

def comment(request):
	Comment.objects.create(comment=request.POST['comment'],user=User.objects.get(id=request.session['logged_in']),message=Message.objects.get(id=request.POST['message_ID']) )
	return redirect('/success')

def delete_comment(request,id):
	c = Comment.objects.get(id=id)
	print(c)
	c.delete()
	return redirect('/success') 






