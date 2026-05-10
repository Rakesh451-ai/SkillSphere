from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Goal
from .forms import GoalForm


@login_required
def goal_list(request):
    goals = Goal.objects.filter(user=request.user)
    pending = goals.filter(status='pending').count()
    in_progress = goals.filter(status='in_progress').count()
    completed = goals.filter(status='completed').count()
    return render(request, 'goals/goal_list.html', {
        'goals': goals,
        'pending': pending,
        'in_progress': in_progress,
        'completed': completed,
    })


@login_required
def goal_add(request):
    if request.method == 'POST':
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            messages.success(request, f'Goal "{goal.title}" created!')
            return redirect('goals:list')
    else:
        form = GoalForm()
    return render(request, 'goals/goal_form.html', {'form': form, 'title': 'Create Goal'})


@login_required
def goal_edit(request, pk):
    goal = get_object_or_404(Goal, pk=pk, user=request.user)
    old_status = goal.status
    if request.method == 'POST':
        form = GoalForm(request.POST, instance=goal)
        if form.is_valid():
            goal = form.save()
            if goal.status == 'completed' and old_status != 'completed':
                request.user.xp_points += 20
                request.user.save()
            messages.success(request, f'Goal "{goal.title}" updated!')
            return redirect('goals:list')
    else:
        form = GoalForm(instance=goal)
    return render(request, 'goals/goal_form.html', {'form': form, 'title': 'Edit Goal'})


@login_required
def goal_delete(request, pk):
    goal = get_object_or_404(Goal, pk=pk, user=request.user)
    if request.method == 'POST':
        goal.delete()
        messages.success(request, 'Goal deleted.')
        return redirect('goals:list')
    return render(request, 'goals/goal_confirm_delete.html', {'goal': goal})
