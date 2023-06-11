from django.db import models
from django.utils import timezone
import uuid


class User(models.Model):
    USER = "user"
    ADMIN = "admin"
    ROLE_CHOICES = [
        (USER, "user"),
        (ADMIN, "admin")
    ]
    
    user_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    discord_nick = models.CharField(max_length=30)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=USER)

    def __str__(self) -> str:
        return f"{self.role.capitalize()}: {self.username}"

class Book(models.Model):
    book_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    summary = models.TextField(max_length=1000, blank=True, default="")
    accepted = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)
    tags = models.ManyToManyField("Tag")
    proposer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="proposer"
    )
    readers = models.ManyToManyField(
        User, default=list, related_name="readers"
    )

    def __str__(self) -> str:
        return f"Book: {self.title}"

class Tag(models.Model):
    tag_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f"Tag: {self.name}"

class Meeting(models.Model):
    meeting_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    meeting_number = models.SmallIntegerField(default=1)
    date = models.DateTimeField(default=timezone.now)
    book_section = models.CharField(max_length=50)
    notes = models.TextField(max_length=1000)
    transcription = models.TextField(blank=True, default="")
    transcription_url = models.URLField(blank=True, default="")
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    attendees = models.ManyToManyField(
        User, blank=True, default=list
    )

    def __str__(self) -> str:
        return f"Meeting: {self.book.title if self.book else '(Book Missing)'}, meeting {self.meeting_number}, {self.date}"

class Post(models.Model):
    post_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    title = models.CharField(max_length=100, blank=True, default="<Untitled>")
    content = models.CharField(max_length=10_000)
    timestamp = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(
        Book, on_delete=models.SET_NULL, null=True, default=None
    )
    meeting = models.ForeignKey(
        Meeting, on_delete=models.SET_NULL, null=True, default=None
    )

    def __str__(self) -> str:
        return f"Post by {self.author.username}: {self.title}"
