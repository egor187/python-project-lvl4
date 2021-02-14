from django.test import TestCase
from django.urls import reverse
from users.models import CustomUser
from .models import TaskStatus


class StatusViewTest(TestCase):
    def setUp(self):
        credentials = {'username': 'John', 'password': 'aswdqwerty5'}
        # credentials2 = {'username': 'Bob', 'password': 'aswdqwerty5'}
        CustomUser.objects.create_user(**credentials)
        credentials_login = {'username': 'John', 'password': 'aswdqwerty5'}
        self.client.login(**credentials_login)
        TaskStatus.objects.create(name='GLOBAL')

    def test_create_task(self):
        response_before_creation = self.client.get(reverse('tasks:statuses_list'))
        self.assertEqual(response_before_creation.status_code, 200)
        self.assertQuerysetEqual(response_before_creation.context['object_list'], ['<TaskStatus: GLOBAL>'])
        TaskStatus.objects.create(name='test_status')
        response_after_creation = self.client.get(reverse('tasks:statuses_list'))
        self.assertEqual(response_after_creation.status_code, 200)
        self.assertQuerysetEqual(
            response_after_creation.context['object_list'],
            ['<TaskStatus: GLOBAL>', '<TaskStatus: test_status>']
        )

    def test_update_status(self):
        status_pk = TaskStatus.objects.get(name='GLOBAL').pk
        url = f'/tasks/statuses/{status_pk}/update/'
        response_from_update_form = self.client.get(url)
        self.assertEqual(response_from_update_form.status_code, 200)
        self.client.post(url, {'name': 'NON-GLOBAL'})

        response_after_update = self.client.get(reverse('tasks:statuses_list'))
        self.assertEqual(response_after_update.status_code, 200)
        self.assertContains(response_after_update, TaskStatus.objects.get(name='NON-GLOBAL'))

    def test_delete_status(self):
        status_pk = TaskStatus.objects.get(name='GLOBAL').pk
        url = f'/tasks/statuses/{status_pk}/delete/'
        response_from_delete_form = self.client.get(url)
        self.assertEqual(response_from_delete_form.status_code, 200)
        self.assertEqual(1, len(TaskStatus.objects.all()))
        self.client.delete(url, {'name': 'GLOBAL'})

        response_after_delete = self.client.get(reverse('tasks:statuses_list'))
        self.assertEqual(response_after_delete.status_code, 200)
        self.assertNotEqual(1, CustomUser.objects.all())

    def test_create_status_within_form(self):
        url = reverse('tasks:create_status')
        response_from_create_form = self.client.get(url)
        self.assertEqual(response_from_create_form.status_code, 200)
        self.client.post(url, {'name': 'ANOTHER GLOBAL'})

        response_after_create = self.client.get(reverse('tasks:statuses_list'))
        self.assertEqual(response_after_create.status_code, 200)
        self.assertContains(response_after_create, TaskStatus.objects.get(name='ANOTHER GLOBAL'))