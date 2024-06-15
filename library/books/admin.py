from django.contrib import admin
from .models import Book, Review, Author


class BookInline(admin.TabularInline):
    model = Book
    extra = 0
    fields = ('title', 'author', 'genre', 'year_published', 'description')
    can_delete = True
    show_change_link = True

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    fields = ('book', 'user', 'text', 'rating', 'created_at')
    readonly_fields = ('created_at',)
    can_delete = True
    show_change_link = True

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'bio')
    list_filter = ('name', )
    search_fields = ('name', )
    ordering = ('name',)

    inlines = [BookInline]

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre', 'year_published', 'description')
    list_filter = ('genre', 'year_published')
    search_fields = ('title', 'author', 'description')
    ordering = ('title',)

    inlines = [ReviewInline]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'text', 'rating', 'created_at')
    list_filter = ('book', 'user', 'rating')
    search_fields = ('user', 'text')
    ordering = ('created_at',)
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)
