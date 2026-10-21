from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ProfileForm


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('dashboard:home')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        if username:
            from accounts.models import User
            from django.utils import timezone
            target_user = User.objects.filter(username=username).first()
            if target_user and not target_user.is_active:
                if target_user.suspended_until and timezone.now() >= target_user.suspended_until:
                    target_user.is_active = True
                    target_user.suspended_until = None
                    target_user.suspension_reason = ''
                    target_user.save(update_fields=['is_active', 'suspended_until', 'suspension_reason'])
                    messages.info(request, 'Your temporary suspension period has expired. Your account has been automatically reactivated!')
                elif target_user.suspended_until:
                    until_str = target_user.suspended_until.strftime('%b %d, %Y %I:%M %p')
                    reason = f" Reason: {target_user.suspension_reason}" if target_user.suspension_reason else ""
                    messages.error(request, f'Your account is currently suspended until {until_str}.{reason}')

        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.display_name}!')
            return redirect('dashboard:home')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('landing')


@login_required
def profile_view(request):
    logged_in_user = request.user
    view_username = request.GET.get('username')
    
    is_own_profile = True
    user = logged_in_user
    
    if view_username and view_username != logged_in_user.username:
        from accounts.models import User
        try:
            user = User.objects.get(username=view_username)
            is_own_profile = False
        except User.DoesNotExist:
            user = logged_in_user

    if request.method == 'POST':
        if is_own_profile:
            form = ProfileForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile updated successfully!')
                return redirect('accounts:profile')
        else:
            messages.error(request, "You cannot edit another user's profile.")
            return redirect(f'/accounts/profile/?username={user.username}')
    else:
        form = ProfileForm(instance=user)
        
    context = {
        'profile_user': user,
        'is_own_profile': is_own_profile,
        'form': form,
    }
    return render(request, 'accounts/profile.html', context)
