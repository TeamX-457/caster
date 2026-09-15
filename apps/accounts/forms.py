from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import School, Student, Teacher, User

INPUT_CLASSES = (
    'mt-1 block w-full rounded-md border border-slate-300 px-3 py-2 text-sm '
    'shadow-sm focus:border-brand-navy focus:outline-none focus:ring-1 focus:ring-brand-navy'
)


class StyledFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            existing = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f'{existing} {INPUT_CLASSES}'.strip()


class StyledAuthenticationForm(StyledFormMixin, AuthenticationForm):
    pass


class StudentSignupForm(StyledFormMixin, UserCreationForm):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    school = forms.ModelChoiceField(queryset=School.objects.all(), empty_label='Select your school')
    grade_level = forms.CharField(max_length=50, required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'school', 'grade_level', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.STUDENT
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.school = self.cleaned_data['school']
        user.save()
        Student.objects.create(user=user, grade_level=self.cleaned_data.get('grade_level', ''))
        return user


class SchoolSignupForm(StyledFormMixin, UserCreationForm):
    first_name = forms.CharField(max_length=150, label='Your first name')
    last_name = forms.CharField(max_length=150, label='Your last name')
    email = forms.EmailField(label='Your email')
    school_name = forms.CharField(max_length=200, label='School name')
    school_address = forms.CharField(max_length=255, required=False, label='School address')
    school_contact_email = forms.EmailField(required=False, label='School contact email')

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'username',
            'school_name', 'school_address', 'school_contact_email',
            'password1', 'password2',
        ]

    def clean_school_name(self):
        name = self.cleaned_data['school_name'].strip()
        if School.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError('A school with this name is already registered.')
        return name

    def save(self, commit=True):
        school = School.objects.create(
            name=self.cleaned_data['school_name'],
            address=self.cleaned_data.get('school_address', ''),
            contact_email=self.cleaned_data.get('school_contact_email', ''),
        )
        user = super().save(commit=False)
        user.role = User.Role.SCHOOL_ADMIN
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.school = school
        user.save()
        return user


class AddTeacherForm(StyledFormMixin, UserCreationForm):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    subject_specialty = forms.CharField(max_length=100, required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'subject_specialty', 'password1', 'password2']

    def __init__(self, *args, school=None, **kwargs):
        self.school = school
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.TEACHER
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.school = self.school
        user.save()
        Teacher.objects.create(user=user, subject_specialty=self.cleaned_data.get('subject_specialty', ''))
        return user
