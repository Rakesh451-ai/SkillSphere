from django import forms
from .models import StudyLog


class StudyLogForm(forms.ModelForm):
    class Meta:
        model = StudyLog
        fields = ['topic', 'hours', 'productivity', 'category', 'notes', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
