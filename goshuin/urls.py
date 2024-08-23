from django.urls import path
from . import views

urlpatterns = [
    path('line/callback/', views.line_callback, name='line_callback'),
    path('callback/', views.callback, name='callback'),
]
