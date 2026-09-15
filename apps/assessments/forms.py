from django import forms

from .models import Assessment, Question

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


class AssessmentForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Assessment
        fields = ['title']


class QuestionForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={'placeholder': 'Question text'}),
        }


class ChoiceForm(forms.Form):
    text = forms.CharField(
        max_length=255, required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Choice text', 'class': INPUT_CLASSES}),
    )
    is_correct = forms.BooleanField(required=False)


ChoiceFormSet = forms.formset_factory(ChoiceForm, extra=4)
