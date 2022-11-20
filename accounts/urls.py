from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('accounts/profile/<int:user_pk>/', views.profile),
    path('accounts/profile_image/<int:user_pk>/', views.profile_image)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
