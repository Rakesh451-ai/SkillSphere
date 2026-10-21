from django import forms


class ResumeUploadForm(forms.Form):
    resume_file = forms.FileField(
        help_text='Upload your resume as a PDF file.',
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf'}),
    )
