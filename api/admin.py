from django.contrib import admin
from .models import Chapter, Verse, UserProgress, Bookmark, LastRead

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ['number', 'name', 'sanskrit_name', 'total_verses']
    ordering = ['number']

@admin.register(Verse)
class VerseAdmin(admin.ModelAdmin):
    list_display = ['chapter', 'verse_number']
    list_filter = ['chapter']
    ordering = ['chapter', 'verse_number']

@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'chapter', 'is_completed', 'completed_at']

@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ['user', 'verse', 'bookmarked_at']

@admin.register(LastRead)
class LastReadAdmin(admin.ModelAdmin):
    list_display = ['user', 'verse', 'updated_at']