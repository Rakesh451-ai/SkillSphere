from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ResumeAnalysis
from .forms import ResumeUploadForm
from .analyzer import analyze_resume


@login_required
def resume_upload(request):
    analyses = ResumeAnalysis.objects.filter(user=request.user)[:5]
    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['resume_file']
            if not file.name.endswith('.pdf'):
                messages.error(request, 'Please upload a PDF file.')
                return render(request, 'resumeanalyzer/upload.html', {'form': form, 'analyses': analyses})

            result = analyze_resume(file)
            file.seek(0)

            analysis = ResumeAnalysis.objects.create(
                user=request.user,
                resume_file=file,
                score=result['score'],
                suggestions=result['suggestions'],
                skills_found=result['skills_found'],
                sections_found=result['sections_found'],
                missing_sections=result['missing_sections'],
            )
            messages.success(request, f'Resume analyzed! Score: {analysis.score}/100')
            return render(request, 'resumeanalyzer/result.html', {'analysis': analysis})
    else:
        form = ResumeUploadForm()
    return render(request, 'resumeanalyzer/upload.html', {'form': form, 'analyses': analyses})


@login_required
def resume_result(request, pk):
    analysis = ResumeAnalysis.objects.get(pk=pk, user=request.user)
    return render(request, 'resumeanalyzer/result.html', {'analysis': analysis})
