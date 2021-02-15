from django.test import TestCase
from django.urls import reverse
from users.models import CustomUser
from .models import TaskStatus, Task


class StatusViewTest(TestCase):
    def setUp(self):
        credentials = {'username': 'John', 'password': 'aswdqwerty5'}
        CustomUser.objects.create_user(**credentials)
        credentials_login = {'username': 'John', 'password': 'aswdqwerty5'}
        self.client.login(**credentials_login)
        TaskStatus.objects.create(name='GLOBAL')

    def test_create_status(self):
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
        # To use reverse with dynamic routes as <int:pk> reverse() takes positional "args" to assign iterable arguments
        # to pass into url-dispatcher
        url = reverse('tasks:update_status', args=(status_pk,))
        response_from_update_form = self.client.get(url)
        self.assertEqual(response_from_update_form.status_code, 200)
        self.client.post(url, {'name': 'NON-GLOBAL'})

        response_after_update = self.client.get(reverse('tasks:statuses_list'))
        self.assertEqual(response_after_update.status_code, 200)
        self.assertContains(response_after_update, TaskStatus.objects.get(name='NON-GLOBAL'))

    def test_delete_status(self):
        status_pk = TaskStatus.objects.get(name='GLOBAL').pk
        url = reverse('tasks:delete_status', args=(status_pk,))
        response_from_delete_form = self.client.get(url)
        self.assertEqual(response_from_delete_form.status_code, 200)
        self.assertEqual(1, len(TaskStatus.objects.all()))
        self.client.delete(url, {'name': 'GLOBAL'})

        response_after_delete = self.client.get(reverse('tasks:statuses_list'))
        self.assertEqual(response_after_delete.status_code, 200)
        self.assertEqual(len(response_after_delete.context['object_list']), TaskStatus.objects.all().count())
        self.assertEqual(1, CustomUser.objects.all().count())

    def test_create_status_within_form(self):
        url = reverse('tasks:create_status')
        response_from_create_form = self.client.get(url)
        self.assertEqual(response_from_create_form.status_code, 200)
        self.client.post(url, {'name': 'ANOTHER GLOBAL'})

        response_after_create = self.client.get(reverse('tasks:statuses_list'))
        self.assertEqual(response_after_create.status_code, 200)
        self.assertContains(response_after_create, TaskStatus.objects.get(name='ANOTHER GLOBAL'))


class TaskViewTest(TestCase):
    def setUp(self):
        credentials = {'username': 'John', 'password': 'aswdqwerty5'}
        user = CustomUser.objects.create_user(**credentials)
        status = TaskStatus.objects.create(name='new')
        self.client.login(**credentials)
        Task.objects.create(name='JUMP', description='JUMP AROUND', task_status=status, creator=user, assigned_to=user)
        return user, status

    def test_create_task(self):
        url = reverse('tasks:tasks_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['object_list'], ['<Task: JUMP>'])
        user = CustomUser.objects.create_user(username='Carl', password='aswdqwerty5')
        status = TaskStatus.objects.create(name='old')
        Task.objects.create(name='RUN', description='RUN AWAY', task_status=status, creator=user, assigned_to=user)
        response_after = self.client.get(url)
        self.assertQuerysetEqual(response_after.context['object_list'], ['<Task: JUMP>', '<Task: RUN>'])
        self.assertContains(response_after, Task.objects.get(name='RUN'))

    def test_update_task(self):
        task_pk = Task.objects.get(name='JUMP').pk
        url_for_update = reverse('tasks:update_task', args=(task_pk,))
        response_for_post = self.client.get(url_for_update)
        self.assertEqual(response_for_post.status_code, 200)
        form = response_for_post.context['form']
        data = form.initial
        data['name'] = 'JAJA'
        self.client.post(url_for_update, data)
        url_for_check = reverse('tasks:tasks_list')
        response_for_check = self.client.get(url_for_check)
        self.assertQuerysetEqual(response_for_check.context['object_list'], ['<Task: JAJA>'])
        self.assertContains(response_for_check, Task.objects.get(name='JAJA'))

    def test_delete_task(self):
        task_pk = Task.objects.get(name='JUMP').pk
        url_for_delete = reverse('tasks:delete_task', args=(task_pk,))
        response_for_delete = self.client.get(url_for_delete)
        self.assertEqual(response_for_delete.status_code, 200)
        self.client.delete(url_for_delete, Task.objects.get(name='JUMP'))
        url_for_check = reverse('tasks:tasks_list')
        response_for_check = self.client.get(url_for_check)
        self.assertQuerysetEqual(response_for_check.context['object_list'], [])
        self.assertNotEqual(1, len(Task.objects.all()))

    def test_create_task_within_form(self):
        url = reverse('tasks:create_task')
        response_from_create_form = self.client.get(url)
        self.assertEqual(response_from_create_form.status_code, 200)
        user = CustomUser.objects.create_user(username='Babe', password='aswdqwerty5')
        status = TaskStatus.objects.create(name='middle')
        self.client.post(url, {'name': 'DANCE', 'description':'DANCING', 'task_status': status, 'creator': user, 'assigned_to': user})
        response_after_create = self.client.get(reverse('tasks:tasks_list'))
        self.assertEqual(response_after_create.status_code, 200)
        self.assertNotContains(response_after_create, ['<Task: DANCE>'])
