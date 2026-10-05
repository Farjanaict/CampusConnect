from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Event, EventRegistration, LostFound, Complaint
from django.contrib import messages

def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect('/login/')

    return render(request, 'register.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('/dashboard/')

    return render(request, 'login.html')
def dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'dashboard.html')

    return redirect('/login/')
def materials(request):
    return render(request, 'materials.html')
def networking(request):
    return render(request, 'networking.html')


def web_engineering(request):
    return render(request, 'web-engineering.html')


def database(request):
    return render(request, 'database.html')
def events(request):
    events = Event.objects.all()
    return render(request, 'events.html', {'events': events})
def register_event(request, event_id):
    if request.user.is_authenticated:
        event = Event.objects.get(id=event_id)

        registration, created = EventRegistration.objects.get_or_create(
            student=request.user,
            event=event
        )

        if created:
            messages.success(request, 'Successfully registered for this event!')
        else:
            messages.warning(request, 'You are already registered for this event.')

        return redirect('/events/')

    return redirect('/login/')

def my_events(request):
    if request.user.is_authenticated:
        registrations = EventRegistration.objects.filter(
            student=request.user
        ).select_related('event')

        return render(request, 'my_events.html', {
            'registrations': registrations
        })

    return redirect('/login/')
def cancel_event(request, event_id):
    if request.user.is_authenticated and request.method == 'POST':

        registration = EventRegistration.objects.filter(
            student=request.user,
            event_id=event_id
        )

        if registration.exists():
            registration.delete()
            messages.success(request, 'Event registration cancelled successfully!')
        else:
            messages.warning(request, 'You are not registered for this event.')

        return redirect('/my-events/')

    return redirect('/login/')
def lost_found(request):
    items = LostFound.objects.all().order_by('-created_at')
    return render(request, 'lost_found.html', {'items': items})


def add_lost_found(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        item_type = request.POST['item_type']
        location = request.POST['location']
        contact = request.POST['contact']

        LostFound.objects.create(
            title=title,
            description=description,
            item_type=item_type,
            location=location,
            contact=contact
        )

        messages.success(request, 'Lost & Found item posted successfully!')
        return redirect('/lost-found/')

    return render(request, 'add_lost_found.html')
def complaints(request):
    if request.user.is_authenticated:
        user_complaints = Complaint.objects.filter(
            student=request.user
        ).order_by('-created_at')

        return render(request, 'complaints.html', {
            'complaints': user_complaints
        })

    return redirect('/login/')


def add_complaint(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            subject = request.POST['subject']
            description = request.POST['description']

            Complaint.objects.create(
                student=request.user,
                subject=subject,
                description=description
            )

            messages.success(request, 'Complaint submitted successfully!')
            return redirect('/complaints/')

        return render(request, 'add_complaint.html')

    return redirect('/login/')
def user_logout(request):
    logout(request)
    return redirect('/login/')