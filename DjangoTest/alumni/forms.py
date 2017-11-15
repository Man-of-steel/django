from django import forms

class LoginForm(forms.Form):
	username = forms.CharField(label='username', max_length=200)
	password = forms.CharField(label='password', max_length=200)
	
class AlumniForm(forms.Form):
	first_name = forms.CharField(max_length=200)
	last_name = forms.CharField(max_length=200)
	email = forms.CharField(max_length=200)
	number = forms.CharField(max_length=200)
	usn = forms.CharField(max_length=200)
	year_of_passing = forms.CharField(max_length=200)
	current_job = forms.CharField(max_length=200)
	password = forms.CharField(max_length=200)
	
class EventForm(forms.Form):
	event_name = forms.CharField(max_length=200)
	from_date = forms.DateField()
	to_date = forms.DateField()
	event_description = forms.CharField(max_length=600)
	
class SignupForm(forms.Form):
	first_name = forms.CharField(max_length=200)
	last_name = forms.CharField(max_length=200)
	email = forms.CharField(max_length=200)
	number = forms.CharField(max_length=200)
	usn = forms.CharField(max_length=200)
	password = forms.CharField(max_length=200)
	year_of_passing = forms.CharField(max_length=200)
	current_job = forms.CharField(max_length=200)
	
class CommentForm(forms.Form):
	comment = forms.CharField(max_length=200)
	event_id = forms.CharField(max_length=10)
	username = forms.CharField(max_length=200)
	
	