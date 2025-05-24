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

class EventCreateView(LoginRequiredMixin, CreateView):
    """View for creating new events"""
    model = Event
    form_class = EventForm
    template_name = 'volunteer/event_form.html'
    
    def form_valid(self, form):
        form.instance.organizer = self.request.user
        messages.success(self.request, "Tạo sự kiện mới thành công!")
        return super().form_valid(form)

class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """View for updating events"""
    model = Event
    form_class = EventForm
    template_name = 'volunteer/event_form.html'
    
    def test_func(self):
        event = self.get_object()
        return self.request.user == event.organizer or self.request.user.is_admin
    
    def form_valid(self, form):
        messages.success(self.request, "Cập nhật sự kiện thành công!")
        return super().form_valid(form)

class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """View for deleting events"""
    model = Event
    template_name = 'volunteer/event_confirm_delete.html'
    success_url = reverse_lazy('home')
    
    def test_func(self):
        event = self.get_object()
        return self.request.user == event.organizer or self.request.user.is_admin
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, "Xóa sự kiện thành công!")
        return super().delete(request, *args, **kwargs)

@login_required
def create_event_report(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.user != event.organizer and not request.user.is_admin:
        messages.error(request, "Bạn không có quyền tạo báo cáo cho sự kiện này.")
        return redirect('event_detail', pk=pk)
    if event.status != 'COM':
        messages.error(request, "Sự kiện chưa kết thúc, không thể tạo báo cáo.")
        return redirect('event_detail', pk=pk)
    try:
        event.report
        messages.info(request, "Sự kiện này đã có báo cáo.")
        return redirect('event_detail', pk=pk)
    except EventReport.DoesNotExist:
        pass

    if request.method == 'POST':
        form = EventReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.event = event
            report.created_by = request.user
            report.save()
            # Xử lý upload nhiều ảnh
            images = request.FILES.getlist('images')
            if len(images) > 10:
                messages.error(request, "Bạn chỉ có thể upload tối đa 10 hình ảnh.")
                return render(request, 'volunteer/report_form.html', {
                    'form': form,
                    'event': event
                })
            for image in images:
                ReportImage.objects.create(report=report, image=image)
            # Cập nhật số giờ tình nguyện cho người tham gia
            participations = EventParticipation.objects.filter(event=event, attended=True)
            for participation in participations:
                user = participation.user
                user.volunteer_hours += event.volunteer_hours
                user.save()
            messages.success(request, "Tạo báo cáo sự kiện thành công!")
            return redirect('event_detail', pk=pk)
    else:
        form = EventReportForm()
    
    return render(request, 'volunteer/report_form.html', {
        'form': form,
        'event': event
    })

@login_required
def update_event_report(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.user != event.organizer and not request.user.is_admin:
        messages.error(request, "Bạn không có quyền chỉnh sửa báo cáo cho sự kiện này.")
        return redirect('event_detail', pk=pk)
    try:
        report = event.report
    except EventReport.DoesNotExist:
        messages.error(request, "Sự kiện này chưa có báo cáo để chỉnh sửa.")
        return redirect('event_detail', pk=pk)

    if request.method == 'POST':
        form = EventReportForm(request.POST, instance=report)
        image_formset = ReportImageFormSet(request.POST, request.FILES, instance=report)
        if form.is_valid():
            form.save()
            # Xử lý xóa ảnh hiện có
            if image_formset.is_valid():
                image_formset.save()
            else:
                messages.error(request, "Có lỗi khi xử lý hình ảnh. Vui lòng kiểm tra lại.")
                return render(request, 'volunteer/report_form.html', {
                    'form': form,
                    'image_formset': image_formset,
                    'event': event
                })
            # Xử lý upload ảnh mới
            images = request.FILES.getlist('images')
            total_images = report.report_images.count() + len(images)
            if total_images > 10:
                messages.error(request, "Tổng số hình ảnh không được vượt quá 10.")
                return render(request, 'volunteer/report_form.html', {
                    'form': form,
                    'image_formset': image_formset,
                    'event': event
                })
            for image in images:
                ReportImage.objects.create(report=report, image=image)
            messages.success(request, "Chỉnh sửa báo cáo sự kiện thành công!")
            return redirect('dashboard')
        else:
            messages.error(request, "Có lỗi trong biểu mẫu. Vui lòng kiểm tra lại.")
    else:
        form = EventReportForm(instance=report)
        image_formset = ReportImageFormSet(instance=report)

    return render(request, 'volunteer/report_form.html', {
        'form': form,
        'image_formset': image_formset,
        'event': event
    })
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

class EventReportView(UserPassesTestMixin, DetailView):
    model = EventReport
    template_name = 'volunteer/event_report.html'
    context_object_name = 'report'

    def test_func(self):
        event = get_object_or_404(Event, pk=self.kwargs['pk'])
        return (
            self.request.user.is_superuser or
            self.request.user == event.organizer
        )

    def get_object(self):
        event_id = self.kwargs['pk']
        event = get_object_or_404(Event, pk=event_id)
        try:
            return EventReport.objects.get(event=event)
        except EventReport.DoesNotExist:
            return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = Event.objects.get(pk=self.kwargs['pk'])
        context['event'] = event
        context['event_ended'] = (event.status == 'COM')
        context['can_modify_report'] = (
            self.request.user.has_perm('volunteer.change_eventreport') or
            self.request.user == event.organizer
        )
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        if self.object is None:
            context['report_exists'] = False
        else:
            context['report_exists'] = True
        return self.render_to_response(context)

class StatisticsView(UserPassesTestMixin, TemplateView):
    template_name = 'volunteer/statistics.html'

    def test_func(self):
        return self.request.user.is_admin  # Chỉ admin mới truy cập được

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Determine the application's root directory (volunteer_project/volunteer/)
        # settings.BASE_DIR usually points to volunteer_project/
        # So, app_static_dir points to volunteer_project/volunteer/static/
        app_static_dir = os.path.join(settings.BASE_DIR, 'volunteer', 'static')
        
        # Define the target directory for charts
        # This will be volunteer_project/volunteer/static/volunteer/image/
        chart_dir = os.path.join(app_static_dir, 'volunteer', 'image')
        
        os.makedirs(chart_dir, exist_ok=True)

        # Định nghĩa ánh xạ trạng thái với tên hiển thị
        status_display_map = dict(Event.EventStatus.choices)

        # 1. Biểu đồ phân loại sự kiện theo trạng thái
        status_counts = Event.objects.values('status').annotate(count=Count('id'))
        statuses = [str(status_display_map[status['status']]) for status in status_counts]
        counts = [status['count'] for status in status_counts]

        # Sử dụng seaborn để làm đẹp biểu đồ
        sns.set_style("whitegrid")
        plt.figure(figsize=(8, 5))  # Giảm chiều cao để đồng bộ kích thước
        bars = plt.bar(statuses, counts, color=sns.color_palette("Blues", len(statuses)), edgecolor='black', linewidth=1.2)

        # Tùy chỉnh giao diện
        plt.title('Phân loại sự kiện theo trạng thái', fontsize=16, pad=20, fontweight='bold', color='#333333')
        plt.xlabel('Trạng thái', fontsize=14, labelpad=10, color='#333333')
        plt.ylabel('Số lượng sự kiện', fontsize=14, labelpad=10, color='#333333')
        plt.xticks(fontsize=12, color='#333333')
        plt.yticks(fontsize=12, color='#333333')
        plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
        # Tùy chỉnh lưới
        plt.grid(True, which='major', axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()

        # Lưu biểu đồ dưới dạng hình ảnh
        status_chart_path = os.path.join(chart_dir, 'status_chart.png')
        plt.savefig(status_chart_path, bbox_inches='tight', dpi=100)
        plt.close()

        # 2. Biểu đồ số lượng sự kiện theo tháng (năm hiện tại)
        current_year = datetime.now().year
        events_by_month = (Event.objects
                          .filter(start_time__year=current_year)
                          .annotate(month=ExtractMonth('start_time'))
                          .values('month')
                          .annotate(count=Count('id'))
                          .order_by('month'))
        
        months = range(1, 13)
        event_counts = [0] * 12
        for entry in events_by_month:
            month = entry['month'] - 1  # Chỉ số bắt đầu từ 0
            event_counts[month] = entry['count']

        # Sử dụng seaborn để làm đẹp biểu đồ
        sns.set_style("whitegrid")
        plt.figure(figsize=(8, 5))  # Giảm chiều cao để đồng bộ kích thước
        plt.plot(months, event_counts, marker='o', color='#007bff', linewidth=2.5, markersize=8, label='Số lượng sự kiện')

        # Tùy chỉnh giao diện
        plt.title(f'Số lượng sự kiện theo tháng (Năm {current_year})', fontsize=16, pad=20, fontweight='bold', color='#333333')
        plt.xlabel('Tháng', fontsize=14, labelpad=10, color='#333333')
        plt.ylabel('Số lượng sự kiện', fontsize=14, labelpad=10, color='#333333')
        plt.xticks(months, ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'], fontsize=12, color='#333333')
        plt.yticks(fontsize=12, color='#333333')
        plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))


        # Tùy chỉnh lưới
        plt.grid(True, which='both', linestyle='--', alpha=0.7)
        plt.legend(fontsize=12)
        plt.tight_layout()

        # Lưu biểu đồ dưới dạng hình ảnh
        monthly_chart_path = os.path.join(chart_dir, 'monthly_chart.png')
        plt.savefig(monthly_chart_path, bbox_inches='tight', dpi=100)
        plt.close()

        # Truyền đường dẫn hình ảnh vào context
        context['status_chart_url'] = 'volunteer/image/status_chart.png'
        context['monthly_chart_url'] = 'volunteer/image/monthly_chart.png'
        return context