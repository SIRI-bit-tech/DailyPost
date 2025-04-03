from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Category, Tag, Author, Article, Comment, Newsletter

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'description')
        }),
        ('SEO', {
            'fields': ('meta_keywords', 'meta_description'),
            'classes': ('collapse',),
        }),
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'website', 'twitter')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name', 'bio')
    raw_id_fields = ('user',)


@admin.register(Article)
class ArticleAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)
    list_display = ('title', 'author', 'category', 'status', 'published_date', 'view_count')
    list_filter = ('status', 'created_date', 'published_date', 'author', 'category')
    search_fields = ('title', 'subtitle', 'content', 'summary')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'published_date'
    save_on_top = True
    filter_horizontal = ('tags',)
    
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'subtitle', 'author', 'category', 'tags', 'status')
        }),
        ('Content', {
            'fields': ('content', 'summary', 'featured_image')
        }),
        ('Publication', {
            'fields': ('published_date',),
            'description': 'You can modify the publication date here.'
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',),
        }),
        ('Social Media', {
            'fields': ('og_title', 'og_description', 'twitter_title', 'twitter_description'),
            'classes': ('collapse',),
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """Custom save to ensure published_date can be modified by admin."""
        # published_date is directly editable in the form
        super().save_model(request, obj, form, change)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'article', 'created_at', 'approved')
    list_filter = ('approved', 'created_at')
    search_fields = ('name', 'email', 'content', 'article__title')
    actions = ['approve_comments']
    
    def approve_comments(self, request, queryset):
        queryset.update(approved=True)
    approve_comments.short_description = "Approve selected comments"


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'confirmed', 'subscribed_date')
    list_filter = ('confirmed', 'subscribed_date')
    search_fields = ('email', 'full_name')
    actions = ['mark_as_confirmed']
    
    def mark_as_confirmed(self, request, queryset):
        queryset.update(confirmed=True)
    mark_as_confirmed.short_description = "Mark selected emails as confirmed"
