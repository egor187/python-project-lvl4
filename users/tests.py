from django.test import TestCase
from django.urls import reverse
from .models import CustomUser


class CreateUserViewTest(TestCase):
    def setUp(self):
        CustomUser.objects.create(username='John', last_name='Lennon')

    def test_creation_user(self):
        response_before_creation = self.client.get(reverse('users:create_user'))
        self.assertEqual(response_before_creation.status_code, 200)
        self.assertTrue(response_before_creation.context)

        response_after_creation = self.client.get(reverse('users:user_list'))
        self.assertEqual(response_after_creation.status_code, 200)
        self.assertContains(response_after_creation, CustomUser.objects.get(username='John'))