from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import StudyLog
from .forms import StudyLogForm


@login_required
def log_list(request):
    logs = StudyLog.objects.filter(user=request.user)
    total_hours = sum(log.hours for log in logs)
    avg_productivity = 0
    if logs:
        avg_productivity = round(sum(log.productivity for log in logs) / len(logs), 1)
    return render(request, 'studylogs/log_list.html', {
        'logs': logs,
        'total_hours': total_hours,
        'avg_productivity': avg_productivity,
    })


@login_required
def log_add(request):
    if request.method == 'POST':
        form = StudyLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.user = request.user
            log.save()
            user = request.user
            today = timezone.now().date()
            if user.last_activity_date == today - timezone.timedelta(days=1):
                user.current_streak += 1
            elif user.last_activity_date != today:
                user.current_streak = 1
            user.last_activity_date = today
            if user.current_streak > user.longest_streak:
                user.longest_streak = user.current_streak
            user.xp_points += 5
            user.save()
            messages.success(request, 'Study log added!')
            return redirect('studylogs:list')
    else:
        form = StudyLogForm(initial={'date': timezone.now().date()})
    return render(request, 'studylogs/log_form.html', {'form': form, 'title': 'Add Study Log'})


@login_required
def log_edit(request, pk):
    log = get_object_or_404(StudyLog, pk=pk, user=request.user)
    if request.method == 'POST':
        form = StudyLogForm(request.POST, instance=log)
        if form.is_valid():
            form.save()
            messages.success(request, 'Study log updated!')
            return redirect('studylogs:list')
    else:
        form = StudyLogForm(instance=log)
    return render(request, 'studylogs/log_form.html', {'form': form, 'title': 'Edit Study Log'})


@login_required
def log_delete(request, pk):
    log = get_object_or_404(StudyLog, pk=pk, user=request.user)
    if request.method == 'POST':
        log.delete()
        messages.success(request, 'Study log deleted.')
        return redirect('studylogs:list')
    return render(request, 'studylogs/log_confirm_delete.html', {'log': log})
