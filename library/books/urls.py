from django.urls import path, include
from . import views

app_name = 'books'

author_patterns = [
    path('', views.AuthorListView.as_view(), name='author_list'),
    path('create/', views.AuthorCreateView.as_view(), name='author_add'),
    path('<int:author_id>/detail', views.AuthorDetailView.as_view(), name='author_detail'),
    path('<int:author_id>/update', views.AuthorUpdateView.as_view(), name='author_update'),
    path('<int:author_id>/delete', views.AuthorDeleteView.as_view(), name='author_delete'),

]

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('<int:book_id>/', views.BookDetailView.as_view(), name='book_detail'),
    path('add/', views.BookCreateView.as_view(), name='book_add'),
    path('<int:book_id>/update/', views.BookUpdateView.as_view(), name='book_update'),
    path('<int:book_id>/delete/', views.BookDeleteView.as_view(), name='book_delete'),
    path('<int:book_id>/reviews/create/', views.ReviewCreateView.as_view(), name='review_create'),
    path('<int:book_id>/reviews/<int:review_id>/update/', views.ReviewUpdateView.as_view(), name='review_update'),
    path('<int:book_id>/reviews/<int:review_id>/delete/', views.ReviewDeleteView.as_view(), name='review_delete'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('author/', include(author_patterns))
]