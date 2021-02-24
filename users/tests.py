from django.test import TestCase
from django.urls import reverse
from .models import CustomUser


class UserViewTest(TestCase):
    def setUp(self):
        credentials = {'username': 'John', 'password': 'aswdqwerty5'}
        CustomUser.objects.create_user(**credentials)
        credentials_login = {'username': 'John', 'password': 'aswdqwerty5'}
        self.client.login(**credentials_login)

    def test_create_user(self):
        response_before_creation = self.client.get(
            reverse('users:create_user')
        )
        self.assertEqual(response_before_creation.status_code, 200)
        response_after_creation = self.client.get(reverse('users:user_list'))
        self.assertEqual(response_after_creation.status_code, 200)
        self.assertContains(
            response_after_creation,
            CustomUser.objects.get(username='John')
        )

    def test_update_user(self):
        user_pk = CustomUser.objects.get(username='John').pk
        url = f'/users/{user_pk}/update/'
        response_from_update_form = self.client.get(url)
        self.assertEqual(response_from_update_form.status_code, 200)
        self.client.post(url, {'username': 'Bob'})

        response_after_update = self.client.get(reverse('users:user_list'))
        self.assertEqual(response_after_update.status_code, 200)
        self.assertContains(
            response_after_update,
            CustomUser.objects.get(username='Bob')
        )

    def test_delete_user(self):
        user_pk = CustomUser.objects.get(username='John').pk
        url = f'/users/{user_pk}/delete/>'
        response_from_delete_form = self.client.get(url)
        self.assertEqual(response_from_delete_form.status_code, 200)
        self.assertEqual(1, len(CustomUser.objects.all()))
        self.client.delete(url, {'username': 'John'})

        response_after_delete = self.client.get(reverse('users:user_list'))
        self.assertEqual(response_after_delete.status_code, 200)
        self.assertNotEqual(1, CustomUser.objects.all())

    def test_create_user_within_form(self):
        url = '/users/create/'
        response_from_create_form = self.client.get(url)
        self.assertEqual(response_from_create_form.status_code, 200)
        self.client.post(
            url,
            {
                'username': 'David',
                'password1': 'level5level5',
                'password2': 'level5level5'
            }
        )

        response_after_update = self.client.get(reverse('users:user_list'))
        self.assertEqual(response_after_update.status_code, 200)
        self.assertContains(
            response_after_update,
            CustomUser.objects.get(username='David')
        )
