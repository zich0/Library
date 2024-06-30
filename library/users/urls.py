from django.urls import path, include
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.UserUpdateView.as_view(), name='user_update'),
    path('favorite/', views.favorite_list, name='favorite_list'),
    path('favorite/<int:favorite_id>/delete/', views.favorite_delete, name='favorite_delete'),
    path('favorite/add/<int:book_id>', views.favorite_add, name='favorite_add'),
]