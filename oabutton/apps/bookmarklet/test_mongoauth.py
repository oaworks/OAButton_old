from django.contrib.auth import authenticate, get_user_model
from django.test import TestCase
from django.test.client import Client
from mongoengine import connect
from mongoengine.errors import NotUniqueError
from nose.plugins.skip import SkipTest
from oabutton.apps.bookmarklet.models import User
from mongoengine.django.mongo_auth.models import (
    MongoUser,
    MongoUserManager,
    get_user_document,
)


class MongoAuthTest(TestCase):
    user_data = {
        'username': 'user',
        'email': 'user@example.com',
        'password': 'some_password',
    }

    def setUp(self):
        connect(db='mongoenginetest')
        User.drop_collection()
        super(MongoAuthTest, self).setUp()

    def test_get_user_model(self):
        self.assertEqual(get_user_model(), MongoUser)

    def test_get_user_document(self):
        self.assertEqual(get_user_document(), User)

    def test_user_manager(self):
        manager = get_user_model()._default_manager
        self.assertTrue(isinstance(manager, MongoUserManager))

    def test_user_manager_exception(self):
        manager = get_user_model()._default_manager
        self.assertRaises(MongoUser.DoesNotExist, manager.get,
                          username='not found')

    def test_create_user(self):
        manager = get_user_model()._default_manager
        user = manager.create_user(**self.user_data)
        self.assertTrue(isinstance(user, User))
        db_user = User.objects.get(username='user')
        self.assertEqual(user.id, db_user.id)

    def test_authenticate(self):
        get_user_model()._default_manager.create_user(**self.user_data)
        user = authenticate(username='user', password='fail')
        self.assertEqual(None, user)
        user = authenticate(username='user', password=self.user_data['password'])
        db_user = User.objects.get(username='user')
        self.assertEqual(user.id, db_user.id)

    def test_unique_users(self):
        manager = get_user_model()._default_manager
        user = manager.create_user(**self.user_data)
        self.assertTrue(isinstance(user, User))

        # Should throw an error
        self.assertRaises(NotUniqueError, manager.create_user, **self.user_data)

    def test_user_bookmarklets(self):
        # Check that we can fetch custom bookmarklets per user_id
        manager = get_user_model()._default_manager
        user = manager.create_user(**self.user_data)
        self.assertTrue(isinstance(user, User))
        db_user = User.objects.get(username='user')
        self.assertEqual(user.id, db_user.id)

        import urlparse
        url = urlparse.urlsplit(user.get_bookmarklet_url())

        c = Client()
        response = c.get(url.path)
        assert response.status_code == 200
        assert "/api/add/?userid=%s&url=" % user.id in response.content

