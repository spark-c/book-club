from django.db import models
import uuid


class User(models.Model):
    user_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    discord_nick = models.CharField(max_length=30)
    role = models.CharField(max_length=20)

    def __str__(self) -> str:
        return f"User: {self.username}"

class Book(models.Model):
    book_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    summary = models.TextField(max_length=1000)
    complete = models.BooleanField(default=False)
    tags = models.ManyToManyField("Tag")
    proposer = models.OneToOneField(User, on_delete=models.SET_NULL)
    readers = models.ManyToManyField(User)

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
    date = models.DateTimeField()
    book_section = models.CharField(max_length=50)
    notes = models.TextField(max_length=1000)
    transcription = models.TextField()
    transcription_url = models.URLField()
    book = models.ForeignKey(Book, on_delete=models.SET_NULL)
    attendees = models.ManyToManyField(User)

    def __str__(self) -> str:
        return f"Meeting: {self.book.title}, meeting {self.meeting_number}, {self.date}"

class Post(models.Model):
    post_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=10_000)
    timestamp = models.DateTimeField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.SET_NULL)
    meeting = models.ForeignKey(Meeting, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return f"Post by {self.author.username}: {self.title}"
