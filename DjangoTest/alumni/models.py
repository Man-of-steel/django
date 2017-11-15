from django.db import models
from django.utils.timezone import now

# Create your models here.
class Admin(models.Model):
	username = models.CharField(max_length = 100)
	password = models.CharField(max_length = 100)

class Alumni(models.Model):	
	first_name = models.CharField(max_length = 100)
	last_name = models.CharField(max_length = 100)
	email = models.CharField(max_length = 500)
	number = models.CharField(max_length = 15)
	usn = models.CharField(max_length = 15, primary_key = True)
	password = models.CharField(max_length = 100)
	year_of_passing = models.IntegerField(default = 0)
	current_job = models.CharField(max_length=100)
	approved = models.BooleanField(default=False)
	
	def getFullName(self):
		return self.first_name + ' ' + self.last_name
	
class EventManager(models.Model):
	id = models.AutoField(primary_key = True)
	name = models.CharField(max_length = 100)
	email = models.CharField(max_length = 100)
	number = models.CharField(max_length = 15)
	password = models.CharField(max_length = 100)
	
	
class Event(models.Model):
	id = models.AutoField(primary_key = True)
	name = models.CharField(max_length = 500)
	from_date = models.DateTimeField()
	to_date = models.DateTimeField()
	event_manager = models.ForeignKey(EventManager, on_delete=models.CASCADE)
	event_description = models.CharField(max_length = 1000)
	
class Comment(models.Model):
	id = models.AutoField(primary_key = True)
	event = models.ForeignKey(Event, on_delete=models.CASCADE)
	username = models.CharField(max_length=200)
	comment = models.CharField(max_length = 1000)
	time = models.DateTimeField(default=now, blank=True)
	
def validate_alumni(email, password):
	alumnis = Alumni.objects.all()
	for alumni in alumnis:
		if(alumni.email == email and alumni.password == password and alumni.approved == True):
			return alumni
	return None

def validate_event_manager(email, password):
	event_managers = EventManager.objects.all()
	for event_manager in event_managers:
		if(event_manager.email == email and event_manager.password == password):
			return event_manager
	return None
	
def create_alumni(form):
	first_name = form.cleaned_data['first_name']
	last_name = form.cleaned_data['last_name']
	number = form.cleaned_data['number']
	usn = form.cleaned_data['usn']
	email = form.cleaned_data['email']
	password = form.cleaned_data['password']
	year_of_passing = form.cleaned_data['year_of_passing']
	current_job = form.cleaned_data['current_job']
	
	new_alumni = Alumni(first_name = first_name, last_name = last_name, email = email, password=password, usn = usn, number = number, year_of_passing = year_of_passing, current_job = current_job)
	
	new_alumni.save()
	
	return True

def create_event(form, event_manager):
	event_name = form.cleaned_data['event_name']
	from_date = form.cleaned_data['from_date']
	to_date = form.cleaned_data['to_date']
	event_description = form.cleaned_data['event_description']
	event = Event(name=event_name, from_date=from_date, to_date=to_date, event_description=event_description, event_manager=event_manager)
	
	event.save()
	
	return True
	
def alumni_signup(form):
	first_name = form.cleaned_data['first_name']
	last_name = form.cleaned_data['last_name']
	email = form.cleaned_data['email']
	number = form.cleaned_data['number']
	usn = form.cleaned_data['usn']
	password = form.cleaned_data['password']
	year_of_passing = form.cleaned_data['year_of_passing']
	current_job = form.cleaned_data['current_job']
	
	alumni = Alumni(first_name=first_name, last_name=last_name, email=email, number=number, usn=usn, password=password, year_of_passing=year_of_passing, current_job=current_job)
	
	alumni.save()
	
	return True
	
def storeComment(form):
	print("Inside store comment function")
	comment = form.cleaned_data['comment']
	username = form.cleaned_data['username']
	event_id = form.cleaned_data['event_id']
	
	comment = Comment(comment=comment, event=Event.objects.get(pk=event_id), username=username)
	
	comment.save()
	
	return True
	
	
	
