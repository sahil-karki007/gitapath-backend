from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Chapter, Verse, UserProgress, Bookmark, LastRead
from .serializers import (
    RegisterSerializer, UserSerializer, ChapterSerializer,
    ChapterListSerializer, VerseSerializer, UserProgressSerializer,
    BookmarkSerializer, LastReadSerializer
)

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_chapters(request):
    chapters = Chapter.objects.all().order_by('number')
    serializer = ChapterListSerializer(chapters, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_chapter(request, chapter_number):
    try:
        chapter = Chapter.objects.get(number=chapter_number)
        serializer = ChapterSerializer(chapter)
        return Response(serializer.data)
    except Chapter.DoesNotExist:
        return Response({'error': 'Chapter not found'}, status=status.HTTP_404_NOT_FOUND)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_verse(request, verse_id):
    try:
        verse = Verse.objects.get(id=verse_id)
        serializer = VerseSerializer(verse)
        return Response(serializer.data)
    except Verse.DoesNotExist:
        return Response({'error': 'Verse not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_progress(request):
    progress = UserProgress.objects.filter(user=request.user)
    serializer = UserProgressSerializer(progress, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_chapter_complete(request, chapter_number):
    try:
        chapter = Chapter.objects.get(number=chapter_number)
        progress, created = UserProgress.objects.get_or_create(
            user=request.user,
            chapter=chapter
        )
        progress.is_completed = True
        progress.completed_at = timezone.now()
        progress.save()
        return Response({'message': 'Chapter marked as complete'})
    except Chapter.DoesNotExist:
        return Response({'error': 'Chapter not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_bookmarks(request):
    bookmarks = Bookmark.objects.filter(user=request.user).order_by('-bookmarked_at')
    serializer = BookmarkSerializer(bookmarks, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_bookmark(request, verse_id):
    try:
        verse = Verse.objects.get(id=verse_id)
        bookmark, created = Bookmark.objects.get_or_create(
            user=request.user,
            verse=verse
        )
        if created:
            return Response({'message': 'Bookmark added'}, status=status.HTTP_201_CREATED)
        return Response({'message': 'Already bookmarked'})
    except Verse.DoesNotExist:
        return Response({'error': 'Verse not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_bookmark(request, verse_id):
    try:
        verse = Verse.objects.get(id=verse_id)
        Bookmark.objects.filter(user=request.user, verse=verse).delete()
        return Response({'message': 'Bookmark removed'})
    except Verse.DoesNotExist:
        return Response({'error': 'Verse not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_last_read(request, verse_id):
    try:
        verse = Verse.objects.get(id=verse_id)
        last_read, created = LastRead.objects.get_or_create(user=request.user)
        last_read.verse = verse
        last_read.save()
        return Response({'message': 'Last read updated'})
    except Verse.DoesNotExist:
        return Response({'error': 'Verse not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_last_read(request):
    try:
        last_read = LastRead.objects.get(user=request.user)
        serializer = LastReadSerializer(last_read)
        return Response(serializer.data)
    except LastRead.DoesNotExist:
        return Response({'message': 'No last read found'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def unmark_chapter_complete(request, chapter_number):
    try:
        chapter = Chapter.objects.get(number=chapter_number)
        UserProgress.objects.filter(
            user=request.user,
            chapter=chapter
        ).update(is_completed=False, completed_at=None)
        return Response({'message': 'Chapter unmarked'})
    except Chapter.DoesNotExist:
        return Response({'error': 'Chapter not found'}, status=status.HTTP_404_NOT_FOUND)    