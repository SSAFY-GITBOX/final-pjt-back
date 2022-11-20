from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('accounts/profile/<int:user_pk>/', views.profile),
    path('accounts/profile_image/<int:user_pk>/', views.profile_image),
    path('accounts/profile_image/<int:user_pk>/follow/', views.follow),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
