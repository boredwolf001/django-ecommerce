from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from .auth import register

urlpatterns = [
    path('', include('shop.urls')),
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    path('auth/login', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('auth/register', register, name='register'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
