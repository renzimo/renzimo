from django.urls import path
from rest_framework import routers

from . import views

urlpatterns = [
    path('summary/', views.SummaryView.as_view())
]
