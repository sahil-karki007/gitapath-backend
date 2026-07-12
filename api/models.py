from django.db import models
from django.contrib.auth.models import User

class Chapter(models.Model):
    number = models.IntegerField(unique=True)
    name = models.CharField(max_length=200)
    sanskrit_name = models.CharField(max_length=200)
    description = models.TextField()
    total_verses = models.IntegerField()

    def __str__(self):
        return f"Chapter {self.number} - {self.name}"

class Verse(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='verses')
    verse_number = models.IntegerField()
    sanskrit = models.TextField()
    hindi = models.TextField()
    english = models.TextField()
    hinglish = models.TextField()

    def __str__(self):
        return f"Chapter {self.chapter.number} - Verse {self.verse_number}"

class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress')
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'chapter')

    def __str__(self):
        return f"{self.user.username} - Chapter {self.chapter.number}"

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    verse = models.ForeignKey(Verse, on_delete=models.CASCADE)
    bookmarked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'verse')

    def __str__(self):
        return f"{self.user.username} bookmarked Verse {self.verse.verse_number}"

class LastRead(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='last_read')
    verse = models.ForeignKey(Verse, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} last read Verse {self.verse.verse_number}"