from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ResumeAnalysis
from .forms import ResumeUploadForm
from .analyzer import analyze_resume


from recommendations.models import Recommendation
from recommendations.engine import generate_recommendations


@login_required
def resume_upload(request):
    if request.GET.get('refresh_recs') == '1':
        generate_recommendations(request.user)

    recommendations = Recommendation.objects.filter(user=request.user)
    if not recommendations.exists():
        generate_recommendations(request.user)
        recommendations = Recommendation.objects.filter(user=request.user)

    analyses = ResumeAnalysis.objects.filter(user=request.user)[:5]
    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['resume_file']
            if not file.name.lower().endswith('.pdf'):
                messages.error(request, 'Please upload a PDF file.')
                return render(request, 'resume_analysis/upload.html', {
                    'form': form,
                    'analyses': analyses,
                    'recommendations': recommendations
                })

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
            return redirect('resume_analysis:result', pk=analysis.pk)
    else:
        form = ResumeUploadForm()
    return render(request, 'resume_analysis/upload.html', {
        'form': form,
        'analyses': analyses,
        'recommendations': recommendations
    })


@login_required
def resume_result(request, pk):
    analysis = get_object_or_404(ResumeAnalysis, pk=pk, user=request.user)
    return render(request, 'resume_analysis/result.html', {'analysis': analysis})
