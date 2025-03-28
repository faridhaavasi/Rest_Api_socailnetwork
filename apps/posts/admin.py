from django.contrib import admin
from apps.posts.models import Post
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'is_published')
    list_filter = ('is_published', 'created_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    list_editable = ('is_published',)
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'image', 'content', 'author')
        }),
        ('Publishing Options', {
            'fields': ('is_published', 'published_at')
        }),
    )
    readonly_fields = ('published_at',)


admin.site.register(Post, PostAdmin)