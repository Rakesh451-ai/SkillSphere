from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


@login_required
def recommendation_list(request):
    if request.GET.get('refresh') == '1':
        return redirect('/resume/?refresh_recs=1')
    return redirect('resume_analysis:upload')
