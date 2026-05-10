from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Skill
from .forms import SkillForm


@login_required
def skill_list(request):
    skills = Skill.objects.filter(user=request.user)
    categories = {}
    for skill in skills:
        cat = skill.get_category_display()
        categories.setdefault(cat, []).append(skill)
    return render(request, 'skills/skill_list.html', {
        'skills': skills,
        'categories': categories,
    })


@login_required
def skill_add(request):
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.user = request.user
            skill.save()
            request.user.xp_points += 10
            request.user.save()
            messages.success(request, f'Skill "{skill.skill_name}" added!')
            return redirect('skills:list')
    else:
        form = SkillForm()
    return render(request, 'skills/skill_form.html', {'form': form, 'title': 'Add Skill'})


@login_required
def skill_edit(request, pk):
    skill = get_object_or_404(Skill, pk=pk, user=request.user)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            skill = form.save()
            skill.update_level()
            skill.save()
            messages.success(request, f'Skill "{skill.skill_name}" updated!')
            return redirect('skills:list')
    else:
        form = SkillForm(instance=skill)
    return render(request, 'skills/skill_form.html', {'form': form, 'title': 'Edit Skill'})


@login_required
def skill_delete(request, pk):
    skill = get_object_or_404(Skill, pk=pk, user=request.user)
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill deleted.')
        return redirect('skills:list')
    return render(request, 'skills/skill_confirm_delete.html', {'skill': skill})
