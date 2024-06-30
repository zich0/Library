from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import UserUpdateForm, UserImageChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from .models import UserImage, Favorite
from django.db.models import Q
from django.core.paginator import Paginator
from books.models import Book


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/user_update_form.html'
    success_url = reverse_lazy('books:book_list')

    def get_object(self, queryset=None):
        return self.request.user


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        try:
            user_image = user.user_image
        except UserImage.DoesNotExist:
            user_image = UserImage.objects.create(user=user)
        context['img_form'] = UserImageChangeForm(instance=user_image)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        user = self.object
        user_form = self.get_form()
        img_form = UserImageChangeForm(request.POST, request.FILES, instance=user.user_image)

        if user_form.is_valid() and img_form.is_valid():
            user_form.save()
            img_form.save()
            return self.form_valid(user_form)
        else:
            return self.form_invalid(user_form)


@login_required
def favorite_list(request):
    sort_by = request.GET.get('sort_by', 'year_published')
    order = request.GET.get('order', 'asc')

    favorites = Favorite.objects.filter(user=request.user).order_by('book__title')

    if sort_by == 'title':
        books = favorites.order_by('-book__title' if order == 'desc' else 'book__title')
    elif sort_by == 'author':
        books = favorites.order_by('-book__author__name' if order == 'desc' else 'book__author__name')
    elif sort_by == 'year_published':
        books = favorites.order_by('-book__year_published' if order == 'desc' else 'book__year_published')

    query = request.GET.get('search')
    if query:
        favorites = Favorite.objects.filter(Q(title__iregex=fr'(?i){query}') | Q(author__name__iregex=fr'(?i){query}'))

    paginator = Paginator(books, 5)
    page_number = request.GET.get('page')
    favorites = paginator.get_page(page_number)

    context = {
        'favorites': favorites,
    }
    return render(request, 'users/favorite.html', context)


@login_required
def favorite_delete(request, favorite_id):
    favorite = get_object_or_404(Favorite, pk=favorite_id)
    favorite.delete()
    return redirect('users:favorite_list')


@login_required
def favorite_add(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    user = request.user
    try:
        favorite = Favorite.objects.get(user=user, book=book)
        favorite.delete()
    except Favorite.DoesNotExist:
        Favorite.objects.create(user=user, book=book)
    return redirect('books:book_list')
