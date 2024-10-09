from django.urls import path
from . import views

urlpatterns = [
    path('set-csrf-token/', views.set_csrf_token, name='set-csrf-token'),
    path('landmarks/', views.generate_landmark_description, name='generate-landmark-description'),
        path('log-frontend-error/', views.log_frontend_error, name='log-frontend-error'),


]
