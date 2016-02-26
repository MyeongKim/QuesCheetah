from django.test import TestCase, Client
from main.models import User, ApiKey, Domain

import json

class MainTestCase(TestCase):
    @classmethod
    def setUp(cls):
        cls.u = User.objects.create(email="test@test.com", username="test")
        cls.u.set_password("123")
        cls.a = ApiKey.objects.generate(cls.u)
        cls.a.secret_key = ApiKey.objects.generate_secret()
        cls.a.save()
        cls.d = Domain.objects.create(domain="asdf.co.kr", api_key=cls.a)

        cls.c = Client()

    def test_user_was_created(self):
        """Check if user exists."""
        created_user = User.objects.get(username="test")
        self.assertEqual(created_user.email, "test@test.com")

    def test_api_key_was_created(self):
        """Check if secret_key and api_key value is created."""
        self.assertIsNotNone(self.a.secret_key)
        self.assertIsNotNone(self.a.key)

    def test_login(self):
        self.c.login(username="test@test.com", password="123")

    def test_domain_was_added(self):
        """Check domain is added correctly to the api_key."""
        self.assertEqual(self.a.domains.count(), 1)

    def test_jwt_was_created(self):
        """Create valid jwt token"""
        response = self.c.post('/jwt/new', json.dumps({"api-key":self.a.key, "secret-key": self.a.secret_key}), content_type='application/json')
        self.assertJSONNotEqual(
            str(response.content, encoding='utf8'),
            {'error': 'Not valid secret key.'}
        )
