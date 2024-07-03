from django.urls import path, include
from . import views

app_name = 'books'

author_patterns = [
    path('', views.author_list, name='author_list'),
    path('<int:author_id>/detail', views.AuthorDetailView.as_view(), name='author_detail'),
]

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('<int:book_id>/', views.BookDetailView.as_view(), name='book_detail'),
    path('<int:book_id>/reviews/create/', views.ReviewCreateView.as_view(), name='review_create'),
    path('<int:book_id>/reviews/<int:review_id>/update/', views.ReviewUpdateView.as_view(), name='review_update'),
    path('<int:book_id>/reviews/<int:review_id>/delete/', views.ReviewDeleteView.as_view(), name='review_delete'),
    path('author/', include(author_patterns)),
    path('genres/', views.GenreListView.as_view(), name='genre_list'),
    path('genres/<int:genre_id>', views.GenreDetailView.as_view(), name='genre_detail'),
]