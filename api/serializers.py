from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Chapter, Verse, UserProgress, Bookmark, LastRead

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class VerseSerializer(serializers.ModelSerializer):
    chapter_number = serializers.IntegerField(source='chapter.number', read_only=True)

    class Meta:
        model = Verse
        fields = ['id', 'verse_number', 'chapter_number', 'sanskrit', 'hindi', 'english']

class ChapterListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ['id', 'number', 'name', 'sanskrit_name', 'description', 'total_verses']

class ChapterSerializer(serializers.ModelSerializer):
    verses = serializers.SerializerMethodField()

    class Meta:
        model = Chapter
        fields = ['id', 'number', 'name', 'sanskrit_name', 'description', 'total_verses', 'verses']

    def get_verses(self, obj):
        verses = obj.verses.all().order_by('verse_number')
        return VerseSerializer(verses, many=True).data

class UserProgressSerializer(serializers.ModelSerializer):
    chapter = ChapterListSerializer(read_only=True)

    class Meta:
        model = UserProgress
        fields = ['id', 'chapter', 'is_completed', 'completed_at']

class BookmarkSerializer(serializers.ModelSerializer):
    verse = VerseSerializer(read_only=True)

    class Meta:
        model = Bookmark
        fields = ['id', 'verse', 'bookmarked_at']

class LastReadSerializer(serializers.ModelSerializer):
    verse = VerseSerializer(read_only=True)

    class Meta:
        model = LastRead
        fields = ['id', 'verse', 'updated_at']