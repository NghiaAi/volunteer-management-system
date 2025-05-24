from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate
from django.forms import inlineformset_factory
from .models import CustomUser, Event, EventReport, ReportImage

class CustomUserCreationForm(UserCreationForm):
    """Form for user registration"""
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'age', 
                 'phone_number', 'address', 'skills', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Tùy chỉnh nhãn và placeholder nếu cần
        self.fields['username'].widget.attrs.update({'placeholder': 'Nhập tên đăng nhập', 'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Nhập email', 'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Nhập họ', 'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Nhập tên', 'class': 'form-control'})
        self.fields['phone_number'].widget.attrs.update({'placeholder': 'Nhập số điện thoại', 'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Nhập mật khẩu', 'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Xác nhận mật khẩu', 'class': 'form-control'})

class CustomUserChangeForm(UserChangeForm):
    old_password = forms.CharField(
        label="Mật khẩu cũ",
        widget=forms.PasswordInput,
        required=False,
        help_text="Nhập mật khẩu hiện tại để xác thực trước khi đổi mật khẩu mới."
    )
    password1 = forms.CharField(
        label="Mật khẩu mới",
        widget=forms.PasswordInput,
        required=False,
        help_text="Để trống nếu không muốn thay đổi mật khẩu."
    )
    password2 = forms.CharField(
        label="Xác nhận mật khẩu",
        widget=forms.PasswordInput,
        required=False,
        help_text="Nhập lại mật khẩu mới để xác nhận."
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'age', 'phone_number', 'address', 'skills', 'volunteer_hours', 'old_password', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Tùy chỉnh nhãn và placeholder nếu cần
        self.fields['username'].widget.attrs.update({'placeholder': 'Nhập tên đăng nhập', 'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Nhập email', 'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Nhập họ', 'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Nhập tên', 'class': 'form-control'})
        self.fields['age'].widget.attrs.update({'placeholder': 'Nhập tuổi', 'class': 'form-control'})
        self.fields['phone_number'].widget.attrs.update({'placeholder': 'Nhập số điện thoại', 'class': 'form-control'})
        self.fields['address'].widget.attrs.update({'placeholder': 'Nhập địa chỉ', 'class': 'form-control'})
        self.fields['skills'].widget.attrs.update({'placeholder': 'Nhập kỹ năng', 'class': 'form-control'})
        self.fields['volunteer_hours'].widget.attrs.update({'placeholder': 'Nhập số giờ tình nguyện', 'class': 'form-control'})
        self.fields['old_password'].widget.attrs.update({'placeholder': 'Nhập mật khẩu cũ', 'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Nhập mật khẩu mới', 'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Xác nhận mật khẩu mới', 'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get("old_password")
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        # Nếu người dùng nhập mật khẩu mới, yêu cầu mật khẩu cũ và xác nhận mật khẩu
        if password1 or password2:
            if not old_password:
                self.add_error('old_password', "Vui lòng nhập mật khẩu cũ để xác thực.")
            else:
                # Kiểm tra mật khẩu cũ có đúng không
                user = authenticate(username=self.instance.username, password=old_password)
                if user is None:
                    self.add_error('old_password', "Mật khẩu cũ không đúng.")
            
            # Kiểm tra mật khẩu mới và xác nhận mật khẩu có khớp không
            if password1 and password2 and password1 != password2:
                self.add_error('password2', "Mật khẩu xác nhận không khớp.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password1 = self.cleaned_data.get("password1")
        if password1:
            user.set_password(password1)  # Mã hóa và cập nhật mật khẩu
        if commit:
            user.save()
        return user

class EventForm(forms.ModelForm):
    """Form for creating and updating events"""
    
    class Meta:
        model = Event
        fields = ['name', 'category', 'start_time', 'end_time', 'location', 
                 'description', 'volunteer_hours', 'max_participants', 'cover_image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 5}),
        }

