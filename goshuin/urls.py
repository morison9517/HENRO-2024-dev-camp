from django.urls import path
from . import views

urlpatterns = [
    path('line/callback/', views.line_callback, name='line_callback'),
    path('callback/', views.callback, name='callback'),
    path('my_view/', views.my_view, name='my_view'),
]
