from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum, Count
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import logout
from django.views.generic import TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Count
from django.db.models.functions import ExtractMonth
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import os
import seaborn as sns
from django.conf import settings

from .models import CustomUser, Event, EventParticipation, EventReport, ReportImage
from .forms import (
    CustomUserCreationForm, CustomUserChangeForm, 
    EventForm, EventReportForm, EventSearchForm, ReportImageFormSet
)

class HomeView(ListView):
    """Home page view with list of events"""
    model = Event
    template_name = 'volunteer/home.html'
    context_object_name = 'events'
    paginate_by = 6
    
    def get_queryset(self):
        queryset = super().get_queryset().order_by('-created_at')
        form = EventSearchForm(self.request.GET)
        if form.is_valid():
            query = form.cleaned_data.get('query')
            category = form.cleaned_data.get('category')
            status = form.cleaned_data.get('status')
            if query:
                queryset = queryset.filter(
                    Q(name__icontains=query) | 
                    Q(description__icontains=query) | 
                    Q(location__icontains=query)
                )
            if category:
                queryset = queryset.filter(category=category)
            if status:
                queryset = queryset.filter(status=status)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = EventSearchForm(self.request.GET)
        context['upcoming_events'] = Event.objects.filter(
            status__in=['PLA', 'ONG']
        ).order_by('start_time')[:5]
        # Thêm form đăng ký vào context
        context['form'] = CustomUserCreationForm()
        return context

class EventDetailView(DetailView):
    """Detail view for a specific event"""
    model = Event
    template_name = 'volunteer/event_detail.html'
    context_object_name = 'event'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['is_participating'] = EventParticipation.objects.filter(
                user=self.request.user, 
                event=self.object
            ).exists()
            context['has_liked'] = self.object.likes.filter(
                id=self.request.user.id
            ).exists()
        if self.object.status == 'COM' and self.request.user.is_authenticated:
            if self.request.user == self.object.organizer or self.request.user.is_admin:
                try:
                    report = self.object.report
                    context['event_report'] = report
                except EventReport.DoesNotExist:
                    context['report_form'] = EventReportForm()
        return context
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user.is_authenticated:
            self.object.viewers.add(request.user)
        context = self.get_context_data()
        # Trả về JSON nếu là yêu cầu AJAX
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'participant_count': self.object.participant_count(),
                'view_count': self.object.viewers.count()
            })
        return self.render_to_response(context)

@login_required
def join_event(request, pk):
    """View for joining an event"""
    event = get_object_or_404(Event, pk=pk)
    if EventParticipation.objects.filter(user=request.user, event=event).exists():
        return JsonResponse({'error': 'Bạn đã đăng ký tham gia sự kiện này rồi.'})
    if event.participants.count() >= event.max_participants and event.max_participants > 0:
        return JsonResponse({'error': 'Sự kiện đã đủ người tham gia.'})
    EventParticipation.objects.create(user=request.user, event=event)
    return JsonResponse({
        'success': 'Đăng ký tham gia sự kiện thành công!',
        'participant_count': event.participant_count()
    })

@login_required
def leave_event(request, pk):
    """View for leaving an event"""
    event = get_object_or_404(Event, pk=pk)
    participation = EventParticipation.objects.filter(user=request.user, event=event).first()
    if not participation:
        return JsonResponse({'error': 'Bạn chưa đăng ký tham gia sự kiện này.'})
    participation.delete()
    return JsonResponse({
        'success': 'Đã hủy đăng ký tham gia sự kiện.',
        'participant_count': event.participant_count()
    })

@login_required
def like_event(request, pk):
    """View for liking/unliking an event"""
    event = get_object_or_404(Event, pk=pk)
    if event.likes.filter(id=request.user.id).exists():
        event.likes.remove(request.user)
        liked = False
    else:
        event.likes.add(request.user)
        liked = True
    return JsonResponse({
        'liked': liked,
        'like_count': event.likes.count()
    })

@login_required
def share_event(request, pk):
    """View for tracking event shares"""
    event = get_object_or_404(Event, pk=pk)
    event.shares += 1
    event.save()
    return JsonResponse({
        'shares': event.shares
    })


class SignUpView(CreateView):
    """View for user registration"""
    form_class = CustomUserCreationForm
    template_name = 'volunteer/signup.html'
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        messages.success(self.request, "Đăng ký tài khoản thành công! Vui lòng đăng nhập.")
        return super().form_valid(form)

class CustomLoginView(LoginView):
    """Custom login view"""
    template_name = 'volunteer/login.html'
    redirect_authenticated_user = True

class ProfileView(LoginRequiredMixin, DetailView):
    """User profile view"""
    model = CustomUser
    template_name = 'volunteer/profile.html'
    context_object_name = 'profile_user'
    
    def get_object(self):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['participating_events'] = user.participating_events.all().order_by('-start_time')
        context['organized_events'] = user.organized_events.all().order_by('-created_at')
        return context

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """View for updating user profile"""
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'volunteer/profile_update.html'
    success_url = reverse_lazy('profile')
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, "Cập nhật thông tin cá nhân thành công!")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Có lỗi xảy ra. Vui lòng kiểm tra lại thông tin.")
        return super().form_invalid(form)


class DashboardView(ListView):
    """Dashboard view for users to see their events or all events if not logged in"""
    model = Event
    template_name = 'volunteer/dashboard.html'
    context_object_name = 'events'

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-created_at')
        form = EventSearchForm(self.request.GET)
        tab = self.request.GET.get('tab', 'all')
        if form.is_valid():
            query = form.cleaned_data.get('query')
            category = form.cleaned_data.get('category')
            status = form.cleaned_data.get('status')
            if query:
                queryset = queryset.filter(
                    Q(name__icontains=query) |
                    Q(description__icontains=query) |
                    Q(location__icontains=query)
                )
            if category:
                queryset = queryset.filter(category=category)
            if status:
                queryset = queryset.filter(status=status)
        if self.request.user.is_authenticated:
            user = self.request.user
            if tab == 'joined':
                queryset = queryset.filter(participants=user)
            elif tab == 'not_joined':
                queryset = queryset.exclude(participants=user)
            elif tab == 'liked':
                queryset = queryset.filter(likes=user)
            elif tab == 'for_you':
                if user.skills:
                    queryset = queryset.filter(category__in=user.skills.split(','))
            elif tab == 'all':
                pass
            else:
                queryset = queryset.filter(Q(organizer=user) | Q(participants=user)).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = EventSearchForm(self.request.GET)
        if self.request.user.is_authenticated:
            user = self.request.user
            context['participating_events'] = user.participating_events.all().order_by('-start_time')
            context['organized_events'] = user.organized_events.all().order_by('-created_at')
            context['liked_events'] = user.liked_events.all().order_by('-created_at')
        return context

def donate(request):
    return render(request, 'volunteer/donate.html')

def custom_logout(request):
    logout(request)
    return redirect('home')

