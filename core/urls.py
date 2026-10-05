from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('materials/', views.materials, name='materials'),
    path('materials/networking/', views.networking, name='networking'),
    path('materials/web-engineering/', views.web_engineering, name='web-engineering'),
    path('materials/database/', views.database, name='database'),

    path('events/', views.events, name='events'),
    path('events/register/<int:event_id>/', views.register_event, name='register_event'),
    path('my-events/', views.my_events, name='my_events'),
    path('events/cancel/<int:event_id>/', views.cancel_event, name='cancel_event'),

    path('lost-found/', views.lost_found, name='lost_found'),
    path('add-lost-found/', views.add_lost_found, name='add_lost_found'),
    path('complaints/', views.complaints, name='complaints'),
path('add-complaint/', views.add_complaint, name='add_complaint'),
]