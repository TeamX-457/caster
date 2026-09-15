from django import forms

from apps.accounts.models import Student

from .models import LearningActivity, StudyGuide

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


class StudyGuideForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = StudyGuide
        fields = ['subject', 'topic', 'title', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10}),
        }


class LearningActivityForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = LearningActivity
        fields = ['activity_type', 'title', 'instructions', 'order']
        widgets = {
            'instructions': forms.Textarea(attrs={'rows': 4}),
        }


class AssignStudyGuideForm(forms.Form):
    students = forms.ModelMultipleChoiceField(
        queryset=Student.objects.none(),
        widget=forms.CheckboxSelectMultiple,
    )

    def __init__(self, *args, school=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['students'].queryset = Student.objects.filter(user__school=school).select_related('user')
