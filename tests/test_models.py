import pytest
from django.utils.timezone import now
from faker import Faker
import copy
from typing import cast
from clubsite.models import (
    User, Book, Tag, Meeting, Post
)


@pytest.mark.django_db
class TestUserModel:
    SIMPLE_USER = {
        "username": "Test User",
        "password": "testpassword",
        "discord_nick": "sparksie",
        "role": User.USER
    }
    SIMPLE_ADMIN = {
        "username": "Test User",
        "password": "testpassword",
        "discord_nick": "sparksie",
        "role": User.ADMIN
    }
    
    def make_user(self, template):
        user = User(
            username=template["username"],
            password=template["password"],
            discord_nick=template["discord_nick"],
            role=template["role"],
        )
        return user
    
    def test_create_user(self):
        user = self.make_user(self.SIMPLE_USER)
        user.save()
        assert User.objects.all()

    def test_create_two_users(self):
        u1 = self.make_user(self.SIMPLE_USER)
        u1.save()

        u2_config = copy.deepcopy(self.SIMPLE_USER)
        u2_config["username"] = "Second User"
        u2 = self.make_user(u2_config)
        u2.save()

        users = User.objects.all()
        assert users[0].username == "Test User"
        assert users[1].username == "Second User"

    def test_create_admin(self):
        u = self.make_user(self.SIMPLE_ADMIN)
        u.save()

        assert User.objects.get(role=User.ADMIN)

    def test_update_user(self):
        u = self.make_user(self.SIMPLE_USER)
        u.save()
        u2 = User.objects.all()[0]

        new_name = "Hello world"
        u2.username = new_name
        u2.save()

        assert User.objects.all()[0].username == new_name

            
@pytest.mark.django_db
class TestBookModel:
    SIMPLE_BOOK = {
            "title": "Blade Runner",
            "author": "Phillip Dick",
            "summary": "Do androids dream\nOf electric sheep??",
            "accepted": False,
            "complete": False,
            "tags": [],
            "proposer": None,
            "readers": [],
        }
    
    def make_book(self, template):
        book = Book(
            title=template["title"],
            author=template["author"],
            summary=template["summary"],
            accepted=template["accepted"],
            complete=template["complete"],
            proposer=template["proposer"],
        )
        return book
    
    def test_create_book(self):
        b = self.make_book(self.SIMPLE_BOOK)
        b.save()

        obj = Book.objects.all()[0]
        assert obj.title == self.SIMPLE_BOOK["title"]
        assert obj.tags.count() == 0
        assert obj.readers.count() == 0

    def test_create_two_books(self):
        b = self.make_book(self.SIMPLE_BOOK)
        b.save()

        new_title = "Second Title"
        book2 = copy.deepcopy(self.SIMPLE_BOOK)
        book2["title"] = new_title
        c = self.make_book(book2)
        c.save()

        books = Book.objects.all()
        assert books[0].title == self.SIMPLE_BOOK["title"]
        assert books[1].title == book2["title"]

    def test_add_proposer(self):
        b = self.make_book(self.SIMPLE_BOOK)
        b.save()

        u = TestUserModel.make_user(TestUserModel(), TestUserModel.SIMPLE_USER)
        u.save()

        b.proposer = u
        b.save()

        book = Book.objects.first()
        assert book is not None and book.proposer is not None # for typechecker
        assert book.proposer.username == TestUserModel.SIMPLE_USER["username"]

    def test_add_tags(self):
        b = self.make_book(self.SIMPLE_BOOK)
        b.save()

        tagname1, tagname2 = ["Feminism", "Greed"]
        t1, t2 = [Tag(name=tagname1), Tag(name=tagname2)]
        t1.save()
        t2.save()

        b.tags.add(t1, t2)
        b.save()

        book = Book.objects.first()
        assert book is not None
        assert book.tags.get(name=tagname1)
        assert book.tags.get(name=tagname2)

    def test_remove_tag(self):
        b = self.make_book(self.SIMPLE_BOOK)
        b.save()

        tagname1, tagname2 = ["Feminism", "Greed"]
        t1, t2 = [Tag(name=tagname1), Tag(name=tagname2)]
        t1.save()
        t2.save()

        book = Book.objects.first()
        assert book is not None
        book.tags.add(t1, t2)
        book.save()

        book = Book.objects.first()
        assert book is not None
        tag = book.tags.first()
        book.tags.remove(tag)
        assert book.tags.count() == 1

    def test_add_readers(self):
        b = self.make_book(self.SIMPLE_BOOK)
        b.save()

        u1 = TestUserModel.make_user(TestUserModel(), TestUserModel.SIMPLE_USER)
        u2 = TestUserModel.make_user(TestUserModel(), TestUserModel.SIMPLE_ADMIN)
        u1.save()
        u2.save()

        b.readers.add(u1, u2)
        b.save()

        book = Book.objects.first()
        assert book is not None
        assert book.readers.count() == 2
        assert book.readers.get(role=TestUserModel.SIMPLE_ADMIN["role"])
    
    def test_simple_update_book(self):
        b = self.make_book(self.SIMPLE_BOOK)
        b.save()

        c = Book.objects.all()[0]
        c.title = "New Title"
        c.save()

        assert Book.objects.all()[0].title == "New Title"


@pytest.mark.django_db
class TestTagModel:

    def test_create_tag(self):
        name = "Feminism"
        t = Tag(name=name)
        t.save()

        tag = Tag.objects.first()
        assert tag is not None
        assert tag.name == name

    def test_create_two_tags(self):
        name1, name2 = ["Feminism", "Greed"]
        t1, t2 = [Tag(name=name1), Tag(name=name2)]
        t1.save()
        t2.save()

        tags = Tag.objects.all()
        assert tags[0] is not None and tags[1] is not None
        assert len(tags) == 2
        assert tags[1].name == name2


@pytest.mark.django_db
class TestMeetingModel:
    SIMPLE_MEETING = {
        "meeting_number": 2,
        "date": now(),
        "book_section": "Chapter 1-5",
        "notes": "There was a discussion today.\n\n Went well.",
        "transcription": "",
        "transcription_url": ""
    }

    def make_meeting(self, template):
        meeting = Meeting(
            meeting_number=template["meeting_number"],
            date=template["date"],
            book_section=template["book_section"],
            notes=template["notes"]
        )
        return meeting
    
    def test_create_meeting(self):
        m = self.make_meeting(self.SIMPLE_MEETING)
        m.save()

        meeting = Meeting.objects.first()
        assert meeting is not None
        assert meeting.meeting_number == 2

    def test_add_attendees(self):
        m = self.make_meeting(self.SIMPLE_MEETING)
        m.save()

        um = TestUserModel
        u1, u2 = [
            um.make_user(um(), um.SIMPLE_USER),
            um.make_user(um(), um.SIMPLE_ADMIN)
        ]
        u1.save()
        u2.save()

        meeting = Meeting.objects.first()
        assert meeting is not None
        meeting.attendees.add(u1, u2)
        meeting.save()

        meeting2 = Meeting.objects.first()
        assert meeting2 is not None
        assert meeting2.attendees.count() == 2

    def test_remove_attendee(self):
        m = self.make_meeting(self.SIMPLE_MEETING)
        m.save()

        um = TestUserModel
        u1, u2 = [
            um.make_user(um(), um.SIMPLE_USER),
            um.make_user(um(), um.SIMPLE_ADMIN)
        ]
        u1.save()
        u2.save()

        meeting = Meeting.objects.first()
        assert meeting is not None
        meeting.attendees.add(u1, u2)
        meeting.save()

        meeting2 = Meeting.objects.first()
        assert meeting2 is not None
        u_rm = meeting.attendees.get(role=User.USER)
        meeting.attendees.remove(u_rm)
        meeting.save()

        meeting3 = Meeting.objects.first()
        assert meeting3 is not None
        assert meeting.attendees.count() == 1

    def test_add_book(self):
        m = self.make_meeting(self.SIMPLE_MEETING)
        m.save()

        bm = TestBookModel
        b = bm.make_book(bm(), bm.SIMPLE_BOOK)
        b.save()

        assert m is not None
        m.book = b
        m.save()

        meeting = Meeting.objects.first()
        assert meeting is not None and meeting.book is not None
        assert meeting.book.title == bm.SIMPLE_BOOK["title"]

    def test_remove_book(self):
        m = self.make_meeting(self.SIMPLE_MEETING)
        m.save()

        bm = TestBookModel
        b = bm.make_book(bm(), bm.SIMPLE_BOOK)
        b.save()

        assert m is not None
        m.book = b
        m.save()

        meeting = Meeting.objects.first()
        assert meeting is not None and meeting.book is not None
        meeting.book = None
        meeting.save()

        meeting2 = Meeting.objects.first()
        assert meeting2 is not None
        assert meeting2.book is None

    def test_update_meeting(self):
        m = self.make_meeting(self.SIMPLE_MEETING)
        m.save()

        t_url = "https://api.google.com/link"
        meeting = Meeting.objects.first()
        assert meeting is not None
        meeting.transcription_url = t_url
        meeting.save()

        meeting2 = Meeting.objects.first()
        assert meeting2 is not None
        assert meeting2.transcription_url == t_url


@pytest.mark.django_db
class TestPostModel:
    SIMPLE_POST = {
        "title": "A Post Title",
        "content": "A long content\nThat has multiple\n\nLines",
        "timestamp": now()
    }

    def make_post(self, template):
        post = Post(
            title=template["title"],
            content=template["content"],
            timestamp=template["timestamp"]
        )
        return post
    
    def test_create_post(self):
        p = self.make_post(self.SIMPLE_POST)
        p.save()

        post = Post.objects.first()
        assert post is not None
        assert post.title == self.SIMPLE_POST["title"]

    def test_delete_post(self):
        p = self.make_post(self.SIMPLE_POST)
        p.save()

        post = Post.objects.first()
        assert post is not None
        post.delete()
        assert Post.objects.all().count() == 0

    def test_add_author(self):
        p = self.make_post(self.SIMPLE_POST)
        p.save()

        um = TestUserModel
        u = um.make_user(um(), um.SIMPLE_USER)
        u.save()

        p.author = u
        p.save()

        post = Post.objects.first()
        assert post is not None and post.author is not None
        assert post.author.username == um.SIMPLE_USER["username"]

    def test_remove_author(self):
        p = self.make_post(self.SIMPLE_POST)
        p.save()

        um = TestUserModel
        u = um.make_user(um(), um.SIMPLE_USER)
        u.save()

        p.author = u
        p.save()

        post = Post.objects.first()
        assert post is not None and post.author is not None
        post.author = None
        post.save()

        # check we didn't delete user entirely
        assert User.objects.all().count() == 1

        post2 = Post.objects.first()
        assert post2 is not None
        assert post2.author is None

    def test_long_content(self):
        fake = Faker()
        t = fake.text(max_nb_chars=9000)

        long_post = copy.deepcopy(self.SIMPLE_POST)
        long_post["content"] = t
        p = self.make_post(long_post)
        p.save()

        post = Post.objects.first()
        assert post is not None
        assert len(post.content) > 7000

