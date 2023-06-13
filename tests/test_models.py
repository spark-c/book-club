import pytest
from clubsite.models import User, Book, Tag
import copy
from typing import cast


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

    # def test_add_readers(self):
    #     pass

    
    def test_simple_update_book(self):
        b = self.make_book(self.SIMPLE_BOOK)
        b.save()

        c = Book.objects.all()[0]
        c.title = "New Title"
        c.save()

        assert Book.objects.all()[0].title == "New Title"