from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render


def landing_page(request):
    if request.user.is_authenticated:
        from django.shortcuts import redirect
        return redirect('dashboard:home')
    return render(request, 'landing.html')


urlpatterns = [
    path('', landing_page, name='landing'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('recommendations/', include('recommendations.urls')),
    path('resume/', include('resumeanalyzer.urls')),
    path('leaderboard/', include('leaderboard.urls')),
    path('notifications/', include('notifications.urls')),
    path('api/', include('skillsphere.api_urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

