from django.test import TestCase
from nose.plugins.skip import SkipTest

from mongoengine import connect
from mongoengine.errors import NotUniqueError
from oabutton.apps.bookmarklet.models import User
try:
    from django.contrib.auth import authenticate, get_user_model
    from mongoengine.django.mongo_auth.models import (
        MongoUser,
        MongoUserManager,
        get_user_document,
    )
    DJ15 = True
except Exception:
    DJ15 = False


class MongoAuthTest(TestCase):
    user_data = {
        'username': 'user',
        'email': 'user@example.com',
    }

    def setUp(self):
        if not DJ15:
            raise SkipTest('mongo_auth requires Django 1.5')
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
        raise SkipTest("No Authentication as we don't do passwords")

    def test_unique_users(self):
        manager = get_user_model()._default_manager
        user = manager.create_user(**self.user_data)
        self.assertTrue(isinstance(user, User))

        # Should throw an error
        self.assertRaises(NotUniqueError, manager.create_user, **self.user_data)

    def test_user_bookmarklets(self):
        manager = get_user_model()._default_manager
        user = manager.create_user(**self.user_data)
        self.assertTrue(isinstance(user, User))
        db_user = User.objects.get(username='user')
        self.assertEqual(user.id, db_user.id)

        from django.conf import settings
        expected_url = "http://%s/api/bookmarklet/%s.js" % (settings.HOSTNAME, user.id)

        self.assertEqual(user.get_bookmarklet_url(), expected_url)

