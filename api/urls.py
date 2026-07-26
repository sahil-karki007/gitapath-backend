from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    # Auth
    path('register/', views.register, name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/', views.get_user, name='get_user'),

    # Chapters
    path('chapters/', views.get_chapters, name='get_chapters'),
    path('chapters/<int:chapter_number>/', views.get_chapter, name='get_chapter'),

    # Verses
    path('verses/<int:verse_id>/', views.get_verse, name='get_verse'),

    # Progress
    path('progress/', views.get_progress, name='get_progress'),
    path('progress/<int:chapter_number>/complete/', views.mark_chapter_complete, name='mark_complete'),

    # Bookmarks
    path('bookmarks/', views.get_bookmarks, name='get_bookmarks'),
    path('bookmarks/<int:verse_id>/add/', views.add_bookmark, name='add_bookmark'),
    path('bookmarks/<int:verse_id>/remove/', views.remove_bookmark, name='remove_bookmark'),

    # Last Read
    path('last-read/', views.get_last_read, name='get_last_read'),
    path('last-read/<int:verse_id>/update/', views.update_last_read, name='update_last_read'),

    path('progress/<int:chapter_number>/uncomplete/', views.unmark_chapter_complete, name='unmark_complete'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/', views.reset_password, name='reset_password'),
]