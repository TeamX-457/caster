from django import forms

from .models import WaitlistSignup

INPUT_CLASSES = (
    'mt-1 block w-full rounded-md border border-slate-300 px-3 py-2 text-sm '
    'shadow-sm focus:border-brand-navy focus:outline-none focus:ring-1 focus:ring-brand-navy'
)


class WaitlistSignupForm(forms.ModelForm):
    class Meta:
        model = WaitlistSignup
        fields = ['full_name', 'email', 'role', 'school_name', 'message']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Full name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'you@example.com'}),
            'school_name': forms.TextInput(attrs={'placeholder': 'School name (optional)'}),
            'message': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Anything you want us to know? (optional)'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            existing = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f'{existing} {INPUT_CLASSES}'.strip()

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if WaitlistSignup.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already on the waitlist.")
        return email
