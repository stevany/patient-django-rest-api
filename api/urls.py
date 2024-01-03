from django.urls import path
from .views import PatientAPI

urlpatterns = [
    path('', PatientAPI.as_view()),
    path('<str:id>',PatientAPI.as_view()),
]