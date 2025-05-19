from django.urls import path
from . import views

urlpatterns = [
    path('', views.IntroTemplateView.as_view(), name='intro'),
]
