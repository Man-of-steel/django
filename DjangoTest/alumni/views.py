from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import LoginForm, AlumniForm, EventForm, SignupForm, CommentForm
from django.contrib.auth import authenticate
from .models import validate_alumni, create_alumni, validate_event_manager, create_event, alumni_signup, Event, Comment, storeComment, Admin, Alumni
# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the alumni index.")
	
def login(request):
	if(request.method == 'POST'):
		form = LoginForm(request.POST)
		if(form.is_valid()):
			entered_username = form.cleaned_data['username']
			entered_password = form.cleaned_data['password']
			#print("Username " + entered_username + " Entered Password " + entered_password)
			try:
				admin = Admin.objects.get(username=entered_username, password=entered_password)
				if admin is not None:
					return HttpResponse(render(request, 'alumni/admin_home.html'))
			except Exception as e:
				print(str(e))
			
			event_manager = validate_event_manager(email=entered_username, password=entered_password)
			
			if event_manager is not None:
				request.session.set_expiry(10000)
				request.session['event_manager'] = event_manager
				request.session['username'] = event_manager.name
				print('session data after login -> ' + str(request.session.keys()))
				return HttpResponse(render(request, 'alumni/manager_home.html'))
				#return HttpResponseRedirect('manager_home')
			
			user = validate_alumni(email=entered_username, password=entered_password)
			
			if user is not None:
				request.session.set_expiry(10000)
				request.session['alumni'] = user
				request.session['username'] = user.getFullName()
				return HttpResponseRedirect('alumni_home')
			else:
				return HttpResponse("Invalid Credentials")
	else:
		return render(request, 'alumni/login.html')
	
def control(request):
	if(request.method == 'POST'):
		form = AlumniForm(request.POST)
		if(form.is_valid()):
			print ('Calling create alumni')
			flag = create_alumni(form)
			if flag:
				print("Create alumni returned " + str(flag))
				script = '<html><body><script>alert("Alumni Created Successfully!!");window.location.href="control";</script></body></html>'
				return HttpResponse(script)
	else:
		return render(request, 'alumni/control.html')
	
def new_event(request):
	if(request.method == 'POST'):
		print("session keys : " + str(request.session.keys()))
		event_manager = request.session['event_manager']
		form = EventForm(request.POST)
		if(form.is_valid()):			
			flag = create_event(form=form, event_manager=event_manager)
			if flag:
				print('Event Created successfully')
				script = '<html><body><script>alert("Event Created Successfully!!");window.location.href="new_event";</script></body></html>'
				return HttpResponse(script)
	else:
		return render(request, 'alumni/new_event.html')
		
def signup(request):
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if(form.is_valid()):
			flag = alumni_signup(form)
			if flag:
				script = '<html><body><script>alert("Signup successful!! You can login once admin approves you...");window.location.href="signup";</script></body></html>'
				return HttpResponse(script)
	else:
		return render(request, 'alumni/signup.html')

def events(request):
	events = Event.objects.all()
	print("Events -> " + str(events) + " length -> " + str(len(events)))
	context = {"events": events}
	if request.path == '/alumni/manager_events':
		return render(request, 'alumni/manager_events.html', context)
	if request.path == '/alumni/alumni_events':
		return render(request, 'alumni/alumni_events.html', context)
	
def event_details(request):
	if(request.method == 'POST'):
		print("Inside event_details function")
		form = CommentForm(request.POST)
		if form.is_valid():
			flag = storeComment(form)
			if flag:
				script = '<html><body><script>alert("Comment posted successfully");window.location.href="manager_events";</script></body></html>'
				return HttpResponse(script)
			else:
				print('Store comment returned False')
		else:
			print("Invalid form")
	else:
		id = request.GET.get('id', '')
		event = Event.objects.get(pk=id)
		print("time -> " + str(event.from_date))
		comments = Comment.objects.filter(event_id=id)
		context = {"id":id, "event": event, "comments":comments}
		return render(request, 'alumni/event_details.html', context)
			
def alumni_event_details(request):
	if(request.method == 'POST'):
		form = CommentForm(request.POST)
		if form.is_valid():
			flag = storeComment(form)
			if flag:
				script = '<html><body><script>alert("Comment posted successfully");window.location.href="alumni_events";</script></body></html>'
				return HttpResponse(script)
			else:
				print('Store comment returned False')
		else:
			print("Invalid form")
	else:
		id = request.GET.get('id', '')
		event = Event.objects.get(pk=id)
		print("time -> " + str(event.from_date))
		comments = Comment.objects.filter(event_id=id)
		context = {"id":id, "event": event, "comments":comments}
		return render(request, 'alumni/alumni_event_details.html', context)
	
def admin_alumni(request):
	usn = request.GET.get('usn', '')
	if(usn != ''):
		Alumni.objects.filter(pk=usn).update(approved=True)
		script = '<html><body><script>alert("Alumni approved successfully");window.location.href="admin_alumni";</script></body></html>'
		return HttpResponse(script)
	print("Skipped if part")
	new_alumni = Alumni.objects.filter(approved=False)
	context = {"new_alumni":new_alumni}
	return render(request, 'alumni/admin_alumni.html', context)
	
def alumni_profile(request):
	if(request.method == 'POST'):
		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')
		email = request.POST.get('email')
		number = request.POST.get('number')
		usn = request.POST.get('usn')
		password = request.POST.get('password')
		year_of_passing = request.POST.get('year_of_passing')
		current_job = request.POST.get('current_job')
		
		Alumni.objects.filter(pk=usn).update(first_name=first_name, last_name=last_name, number=number, email=email, password=password, year_of_passing=year_of_passing, current_job=current_job)
		
		script = '<html><body><script>alert("Profile updated successfully, Changes will be reflected when you logout");window.location.href="alumni_profile";</script></body></html>'
		return HttpResponse(script)	
	else:
		return render(request, 'alumni/alumni_profile.html')
	
		
def redirect(request):
	print("Obtained Path " + request.path)
	if(request.path == '/alumni/login'):
		return login(request)
	if(request.path == '/alumni/alumni_home'):
		return render(request, 'alumni/alumni_home.html')
	if(request.path == '/alumni/manager_home'):
		return render(request, 'alumni/manager_home.html')
	if(request.path == '/alumni/control'):
		return control(request)
	if(request.path == '/alumni/manager_events'):
		return events(request)
	if(request.path == '/alumni/alumni_events'):
		return events(request)
	if(request.path == '/alumni/new_event'):
		return new_event(request)
	if(request.path == '/alumni/signup'):
		return signup(request)
	if(request.path == '/alumni/event_details'):
		return event_details(request)
	if(request.path == '/alumni/alumni_event_details'):
		return alumni_event_details(request)
	if(request.path == '/alumni/admin_home'):
		return render(request, 'alumni/admin_home.html')
	if(request.path == '/alumni/admin_alumni'):
		return admin_alumni(request)
	if(request.path == '/alumni/alumni_profile'):
		return alumni_profile(request)
	
		
				
	