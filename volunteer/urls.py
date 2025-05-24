from django.urls import path
from . import views

urlpatterns = [
    # Main pages
    path('', views.HomeView.as_view(), name='home'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    
    # Authentication
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.custom_logout, name='logout'),  # Use custom_logout function
    
    # Other paths remain unchanged
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/update/', views.ProfileUpdateView.as_view(), name='profile_update'),
    path('donate/', views.donate, name='donate'),
    path('events/<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    path('events/create/', views.EventCreateView.as_view(), name='event_create'),
    path('events/<int:pk>/update/', views.EventUpdateView.as_view(), name='event_update'),
    path('events/<int:pk>/delete/', views.EventDeleteView.as_view(), name='event_delete'),
    path('events/<int:pk>/join/', views.join_event, name='join_event'),
    path('events/<int:pk>/leave/', views.leave_event, name='leave_event'),
    path('events/<int:pk>/like/', views.like_event, name='like_event'),
    path('events/<int:pk>/share/', views.share_event, name='share_event'),
    path('events/<int:pk>/event-report/', views.EventReportView.as_view(), name='event_report'),
    path('events/<int:pk>/create-report/', views.create_event_report, name='create_report'),

]