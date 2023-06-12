import pytest
from clubsite.models import User


@pytest.mark.django_db
class TestUserModel:
    def test_create_user(self):
        user = User(
            username="Test User",
            password="testpassword",
            discord_nick="sparksie",
            role=User.USER
        )
        user.save()
        assert User.objects.all()

    def test_create_two_users(self):
        u1 = User(
            username="Test User",
            password="testpassword",
            discord_nick="sparksie",
            role=User.USER
        )
        u1.save()
        u2 = User(
            username="Test User2",
            password="testpassword2",
            discord_nick="sparksie2",
            role=User.USER
        )
        u2.save()

        assert len(User.objects.all()) == 2

    def test_create_admin(self):
        u = User(
            username="Test User",
            password="testpassword",
            discord_nick="sparksie",
            role=User.ADMIN
        )
        u.save()

        assert User.objects.get(role=User.ADMIN)

    def test_update_user(self):
        u = User(
            username="Test User",
            password="testpassword",
            discord_nick="sparksie",
            role=User.USER
        )
        u.save()
        u2 = User.objects.all()[0]

        new_name = "Hello world"
        u2.username = new_name
        u2.save()

        assert User.objects.all()[0].username == new_name

            