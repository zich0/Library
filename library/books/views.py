from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Book, Review
from .forms import BookForm, ReviewForm, LoginForm, SignupForm
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout


# class AuthorListView(ListView):
#     model = Author
#     template_name = 'books/author_list.html'
#     context_object_name = 'authors'
#
# class AuthorDetailView(DetailView):
#     model = Author
#     template_name = 'books/author_detail.html'
#     pk_url_kwarg = 'author_id'
#
# class AuthorCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
#     model = Author
#     form_class = AuthorForm
#     template_name = 'books/author_form.html'
#
#     def test_func(self):
#         return self.request.user.is_staff
#
#     def get_success_url(self):
#         return reverse('books:author_list')
#
# class AuthorUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#     model = Author
#     form_class = AuthorForm
#     template_name = 'books/author_form.html'
#     pk_url_kwarg = 'author_id'
#
#     def test_func(self):
#         return self.request.user.is_staff
#
#     def get_success_url(self):
#         return reverse('books:author_list')
#
# class AuthorDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
#     model = Book
#     pk_url_kwarg = 'author_id'
#     template_name = 'books/author_confirm_delete.html'
#     success_url = reverse_lazy('books:author_list')
#
#     def test_func(self):
#         return self.request.user.is_staff
def book_list(request):
    sort_by = request.GET.get('sort_by', 'year_published')
    order = request.GET.get('order', 'asc')

    book_list = Book.objects.all().order_by('title')

    is_admin = request.user.is_staff

    if sort_by == 'title':
        book_list = book_list.order_by('-title' if order == 'desc' else 'title')
    elif sort_by == 'author':
        book_list = book_list.order_by('-author' if order == 'desc' else 'author')
    elif sort_by == 'year_published':
        book_list = book_list.order_by('-year_published' if order == 'desc' else 'year_published')

    context = {
        'book_list': book_list,
        'is_admin': is_admin,
    }
    return render(request, 'books/book_list.html', context)

class BookDetailView(DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    pk_url_kwarg = 'book_id'
    context_object_name = 'book'

class BookCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'books/book_form.html'

    def test_func(self):
        return self.request.user.is_staff

    def get_success_url(self):
        return reverse_lazy('books:book_detail', kwargs={'book_id': self.object.id})

class BookUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'books/book_form.html'
    pk_url_kwarg = 'book_id'

    def test_func(self):
        return self.request.user.is_staff

    def get_success_url(self):
        return reverse('books:book_list')

class BookDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Book
    pk_url_kwarg = 'book_id'
    template_name = 'books/book_confirm_delete.html'
    success_url = reverse_lazy('books:book_list')

    def test_func(self):
        return self.request.user.is_staff

class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'books/review_form.html'

    def form_valid(self, form):
        form.instance.book_id = self.kwargs['book_pk']
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('books:book_detail', kwargs={'pk': self.kwargs['book_pk']})

class SignupView(CreateView):
    model = User
    form_class = SignupForm
    template_name = 'base/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('books:book_list')
    else:
        form = LoginForm()
    return render(request, 'base/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('books:book_list')
