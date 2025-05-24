from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


class CustomUser(AbstractUser):
    """Custom user model extending Django's AbstractUser model"""
    age = models.PositiveIntegerField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    skills = models.TextField(blank=True)
    volunteer_hours = models.PositiveIntegerField(default=0)
    is_admin = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username


class Event(models.Model):
    """Model for volunteer events"""
    
    # Event category choices
    class EventCategory(models.TextChoices):
        EDUCATION = 'EDU', _('Giáo dục')
        ENVIRONMENT = 'ENV', _('Môi trường')
        HEALTH = 'HEA', _('Y tế')
        COMMUNITY = 'COM', _('Cộng đồng')
        OTHER = 'OTH', _('Khác')
    
    # Event status choices
    class EventStatus(models.TextChoices):
        PLANNING = 'PLA', _('Đang lên kế hoạch')
        ONGOING = 'ONG', _('Đang diễn ra')
        COMPLETED = 'COM', _('Đã kết thúc')
    
    name = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=200)
    description = models.TextField()
    volunteer_hours = models.PositiveIntegerField(default=0)
    max_participants = models.PositiveIntegerField(default=0)
    cover_image = models.ImageField(upload_to='event_covers/', blank=True, null=True)
    
    category = models.CharField(
        max_length=3,
        choices=EventCategory.choices,
        default=EventCategory.OTHER,
    )
    
    status = models.CharField(
        max_length=3,
        choices=EventStatus.choices,
        default=EventStatus.PLANNING,
    )
    
    organizer = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name='organized_events'
    )
    
    participants = models.ManyToManyField(
        CustomUser, 
        related_name='participating_events',
        through='EventParticipation',
        blank=True
    )
    
    viewers = models.ManyToManyField(
        CustomUser, 
        related_name='viewed_events', 
        blank=True
    )
    
    likes = models.ManyToManyField(
        CustomUser, 
        related_name='liked_events', 
        blank=True
    )
    
    shares = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
        
    def get_absolute_url(self):
        return reverse('event_detail', kwargs={'pk': self.pk})
    
    def view_count(self):
        return self.viewers.count()
    
    def like_count(self):
        return self.likes.count()
    
    def participant_count(self):
        return self.participants.count()


class EventParticipation(models.Model):
    """Model for tracking event participation"""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)
    attended = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['user', 'event']
        
    def __str__(self):
        return f"{self.user.username} - {self.event.name}"


