from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Event, EventRegistration, LostFound, Complaint
from django.contrib import messages
from django.db import IntegrityError

def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        if not username or not password:
            messages.error(request, 'Username and Password are required!')
            return render(request, 'register.html')

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            user.save()
            messages.success(request, 'Account created successfully! Please login.')
            return redirect('/login/')
        except IntegrityError:
            messages.error(request, 'Username already exists! Please choose another one.')
            return render(request, 'register.html')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return render(request, 'register.html')

    return render(request, 'register.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('/dashboard/')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')

    return render(request, 'login.html')


def dashboard(request):
    if request.user.is_authenticated:
        events = Event.objects.all().order_by('-id')[:3]
        lost_found_items = LostFound.objects.all().order_by('-id')[:3]
        user_complaints = Complaint.objects.filter(student=request.user).order_by('-id')[:3]

        context = {
            'events': events,
            'lost_found_items': lost_found_items,
            'complaints': user_complaints,
        }
        return render(request, 'dashboard.html', context)

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
    events = Event.objects.all().order_by('-id')
    return render(request, 'events.html', {'events': events})


def register_event(request, event_id):
    if request.user.is_authenticated:
        try:
            event = Event.objects.get(id=event_id)
            registration, created = EventRegistration.objects.get_or_create(
                student=request.user,
                event=event
            )

            if created:
                messages.success(request, 'Successfully registered for this event!')
            else:
                messages.warning(request, 'You are already registered for this event.')
        except Event.DoesNotExist:
            messages.error(request, 'Event not found.')

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
    items = LostFound.objects.all().order_by('-id')
    return render(request, 'lost_found.html', {'items': items})


def add_lost_found(request):
    if request.method == 'POST':
        title = request.POST.get('title', '')
        description = request.POST.get('description', '')
        item_type = request.POST.get('item_type', '')
        location = request.POST.get('location', '')
        contact = request.POST.get('contact', '')

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
        ).order_by('-id')

        return render(request, 'complaints.html', {
            'complaints': user_complaints
        })

    return redirect('/login/')


def add_complaint(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            subject = request.POST.get('subject', '')
            description = request.POST.get('description', '')

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