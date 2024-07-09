from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Book, Review, Author, Genre
from .forms import BookForm, ReviewForm, AuthorForm
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from users.models import Favorite


def author_list(request):
    sort_by = request.GET.get('sort_by', 'name')
    order = request.GET.get('order', 'asc')

    authors = Author.objects.all()

    if sort_by == 'name':
        authors = authors.order_by('-name' if order == 'desc' else 'name')

    paginator = Paginator(authors, 5)
    page_number = request.GET.get('page')
    authors = paginator.get_page(page_number)

    context = {
        'author_list': authors,
    }

    return render(request, 'books/author_list.html', context)


class AuthorDetailView(DetailView):
    model = Author
    template_name = 'books/author_detail.html'
    pk_url_kwarg = 'author_id'


def book_list(request):
    sort_by = request.GET.get('sort_by', 'year_published')
    order = request.GET.get('order', 'asc')

    books = Book.objects.all().order_by('title')

    is_authenticated = request.user.is_authenticated

    if sort_by == 'title':
        books = books.order_by('-title' if order == 'desc' else 'title')
    elif sort_by == 'author':
        books = books.order_by('-author__name' if order == 'desc' else 'author__name')
    elif sort_by == 'year_published':
        books = books.order_by('-year_published' if order == 'desc' else 'year_published')

    query = request.GET.get('search')
    if query:
        books = Book.objects.filter(Q(title__iregex=fr'(?i){query}') | Q(author__name__iregex=fr'(?i){query}'))

    paginator = Paginator(books, 5)
    page_number = request.GET.get('page')
    books = paginator.get_page(page_number)

    context = {
        'book_list': books,
        'is_authenticated': is_authenticated,
    }

    if is_authenticated:
        context['favorite_list'] = Favorite.objects.filter(user=request.user).values_list('book_id', flat=True)

    return render(request, 'books/book_list.html', context)

class BookDetailView(DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    pk_url_kwarg = 'book_id'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        context['reviews'] = Review.objects.filter(book=book)
        is_authenticated = self.request.user.is_authenticated
        context['is_authenticated'] = is_authenticated
        if is_authenticated:
            context['favorite_list'] = Favorite.objects.filter(user=self.request.user).values_list('book_id', flat=True)
        return context


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'books/review_form.html'

    def form_valid(self, form):
        form.instance.book = get_object_or_404(Book, id=self.kwargs['book_id'])
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('books:book_detail', kwargs={'book_id': self.object.book.id})

class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'books/review_form.html'
    pk_url_kwarg = 'review_id'

    def test_func(self):
        review = self.get_object()
        return review.user == self.request.user

    def get_success_url(self):
        return reverse_lazy('books:book_detail', kwargs={'book_id': self.object.book.id})

class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    model = Review
    template_name = 'books/review_delete.html'
    pk_url_kwarg = 'review_id'
    context_object_name = 'review'

    def test_func(self):
        review = self.get_object()
        return review.user == self.request.user

    def get_success_url(self):
        return reverse_lazy('books:book_detail', kwargs={'book_id': self.object.book.id})


class GenreListView(ListView):
    model = Genre
    template_name = 'books/genre_list.html'
    context_object_name = 'genres'


class GenreDetailView(DetailView):
    model = Genre
    template_name = 'books/genre_detail.html'
    pk_url_kwarg = 'genre_id'
    success_url = reverse_lazy('books:genre_detail')

    def get_context_data(self, **kwargs):
        is_authenticated = self.request.user.is_authenticated
        genre = self.get_object()
        genre_books = genre.books.all()

        paginator = Paginator(genre_books, 5)
        page_number = self.request.GET.get('page')
        genre_books = paginator.get_page(page_number)

        context = {
            'genre': genre,
            'genre_books': genre_books,
            'is_authenticated': is_authenticated,
        }

        if is_authenticated:
            context['favorite_list'] = Favorite.objects.filter(user=self.request.user).values_list('book_id', flat=True)

        return context

