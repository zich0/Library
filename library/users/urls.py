from django.urls import path, include
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.UserUpdateView.as_view(), name='user_update'),

]