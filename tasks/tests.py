from django.test import TestCase
from django.urls import reverse
from users.models import CustomUser
from .models import TaskStatus, Task, Label


class StatusViewTest(TestCase):
    def setUp(self):
        credentials = {'username': 'John', 'password': 'aswdqwerty5'}
        CustomUser.objects.create_user(**credentials)
        credentials_login = {'username': 'John', 'password': 'aswdqwerty5'}
        self.client.login(**credentials_login)
        TaskStatus.objects.create(name='GLOBAL')

    def test_create_status(self):
        response_before_creation = self.client.get(
            reverse('tasks:statuses_list')
        )
        self.assertEqual(response_before_creation.status_code, 200)
        self.assertQuerysetEqual(
            response_before_creation.context['object_list'],
            ['<TaskStatus: GLOBAL>']
        )
        TaskStatus.objects.create(name='test_status')
        response_after_creation = self.client.get(
            reverse('tasks:statuses_list')
        )
        self.assertEqual(response_after_creation.status_code, 200)
        self.assertQuerysetEqual(
            response_after_creation.context['object_list'],
            ['<TaskStatus: GLOBAL>', '<TaskStatus: test_status>']
        )

    def test_update_status(self):
        status_pk = TaskStatus.objects.get(name='GLOBAL').pk
        # To use reverse with dynamic routes as <int:pk> reverse()
        # takes positional "args" to assign iterable arguments
        # to pass into url-dispatcher
        url = reverse('tasks:update_status', args=(status_pk,))
        response_from_update_form = self.client.get(url)
        self.assertEqual(response_from_update_form.status_code, 200)
        self.client.post(url, {'name': 'NON-GLOBAL'})

        response_after_update = self.client.get(reverse('tasks:statuses_list'))
        self.assertEqual(response_after_update.status_code, 200)
        self.assertContains(
            response_after_update,
            TaskStatus.objects.get(name='NON-GLOBAL')
        )

    def test_delete_status(self):
        status_pk = TaskStatus.objects.get(name='GLOBAL').pk
        url = reverse('tasks:delete_status', args=(status_pk,))
        response_from_delete_form = self.client.get(url)
        self.assertEqual(response_from_delete_form.status_code, 200)
        self.assertEqual(1, len(TaskStatus.objects.all()))
        self.client.delete(url)
        response_after_delete = self.client.get(reverse('tasks:statuses_list'))
        self.assertEqual(response_after_delete.status_code, 200)
        self.assertEqual(
            len(
                response_after_delete.context['object_list']
            ),
            TaskStatus.objects.all().count()
        )
        self.assertEqual(1, CustomUser.objects.all().count())
        self.assertQuerysetEqual(
            response_after_delete.context['object_list'],
            []
        )

    def test_create_status_within_form(self):
        url = reverse('tasks:create_status')
        response_from_create_form = self.client.get(url)
        self.assertEqual(response_from_create_form.status_code, 200)
        self.client.post(url, {'name': 'ANOTHER GLOBAL'})
        response_after_create = self.client.get(reverse('tasks:statuses_list'))
        self.assertEqual(response_after_create.status_code, 200)
        self.assertContains(
            response_after_create,
            TaskStatus.objects.get(name='ANOTHER GLOBAL')
        )


class TaskViewTest(TestCase):
    def setUp(self):
        credentials = {'username': 'John', 'password': 'aswdqwerty5'}
        user = CustomUser.objects.create_user(**credentials)
        status = TaskStatus.objects.create(name='new')
        self.client.login(**credentials)
        Task.objects.create(
            name='JUMP',
            description='JUMP AROUND',
            task_status=status,
            creator=user,
            assigned_to=user
        )

    def test_create_task(self):
        url = reverse('tasks:tasks_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['object_list'],
            ['<Task: JUMP>']
        )
        user = CustomUser.objects.create_user(
            username='Carl',
            password='aswdqwerty5'
        )
        status = TaskStatus.objects.create(name='old')
        Task.objects.create(
            name='RUN',
            description='RUN AWAY',
            task_status=status,
            creator=user,
            assigned_to=user
        )
        response_after = self.client.get(url)
        self.assertQuerysetEqual(
            response_after.context['object_list'],
            ['<Task: JUMP>', '<Task: RUN>']
        )
        self.assertContains(response_after, Task.objects.get(name='RUN'))

    # def test_update_task(self):
    #     task_pk = Task.objects.get(name='JUMP').pk
    #     url_for_update = reverse('tasks:update_task', args=(task_pk,))
    #     response_for_post = self.client.get(url_for_update)
    #     self.assertEqual(response_for_post.status_code, 200)
    #     # form = response_for_post.context['form']
    #     # data = form.initial
    #     # data['name'] = 'JAJA'
    #     # self.client.post(url_for_update, data)
    #     status = TaskStatus.objects.create(name='test_status')
    #     Label.objects.create(name='test_label')
    #     label = Label.objects.get(name='test_label')
    #     # task = Task.objects.get(name='JAJA')
    #     # task.label.add(label)
    #     self.client.post(
    #     url_for_update,
        #     {
        #       'name': 'JAJA',
        #       'description': 'test',
        #       'task_status': status,
        #       'creator': 'John',
        #       'assigned_to': 'John'
        #       }
    #       )
    #     task = Task.objects.get(name='JAJA')
    #     task.label.add(label)
    #
    #     url_for_check = reverse('tasks:tasks_list')
    #     response_for_check = self.client.get(url_for_check)
    #     self.assertQuerysetEqual(
    #     response_for_check.context['object_list'],
    #     ['<Task: JAJA>']
    #     )
    #     self.assertContains(
    #     response_for_check,
    #     Task.objects.get(name='JAJA')
    #     )

    def test_delete_task(self):
        task_pk = Task.objects.get(name='JUMP').pk
        url_for_delete = reverse('tasks:delete_task', args=(task_pk,))
        response_for_delete = self.client.get(url_for_delete)
        self.assertEqual(response_for_delete.status_code, 200)
        self.client.delete(url_for_delete)
        url_for_check = reverse('tasks:tasks_list')
        response_for_check = self.client.get(url_for_check)
        self.assertQuerysetEqual(response_for_check.context['object_list'], [])
        self.assertNotEqual(1, len(Task.objects.all()))

    # def test_create_task_within_form(self):
    #     url = reverse('tasks:create_task')
    #     response_from_create_form = self.client.get(url)
    #     self.assertEqual(response_from_create_form.status_code, 200)
    #
    #     Label.objects.create(name='test_label')
    #     label = Label.objects.get(name='test_label')
    #
    #     self.client.post(url, {
    #         'name': 'DANCE',
    #         'description':'DANCING',
    #         'task_status': 'status',
    #         'creator': 'John',
    #         'assigned_to': 'John',
    #         'label': label
    #         }
    #     )
    #
    #     response_after_create = self.client.get(reverse('tasks:tasks_list'))
    #     self.assertEqual(response_after_create.status_code, 200)
    #     self.assertContains(
    #     response_after_create,
    #     Task.objects.get(name='DANCE')
    #     )
    #     self.assertQuerysetEqual(
    #     response_after_create.context['object_list'],
    #     ['<Task: JUMP>', '<Task: DANCE>']
    #     )


class LabelViewTest(TestCase):
    def setUp(self):
        credentials = {'username': 'John', 'password': 'aswdqwerty5'}
        CustomUser.objects.create_user(**credentials)
        self.client.login(**credentials)
        TaskStatus.objects.create(name='new_status')
        Label.objects.create(name='new_label')

    def test_create_label(self):
        url = reverse('tasks:labels_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['object_list'],
            ['<Label: new_label>']
        )
        label = Label.objects.create(name='another_label')
        label.save()
        response_after = self.client.get(url)
        self.assertEqual(response_after.status_code, 200)
        self.assertQuerysetEqual(
            response_after.context['object_list'],
            ['<Label: another_label>', '<Label: new_label>']
        )

    def test_update_label(self):
        label_pk = Label.objects.get(name='new_label').pk
        url_list = reverse('tasks:labels_list')
        url_update = reverse('tasks:update_label', args=(label_pk,))
        response_list = self.client.get(url_list)
        self.assertEqual(response_list.status_code, 200)
        self.assertContains(response_list, Label.objects.get(name='new_label'))
        self.assertQuerysetEqual(
            response_list.context['object_list'],
            ['<Label: new_label>']
        )
        self.client.post(url_update, {'name': 'old_label'})
        response_list_after = self.client.get(url_list)
        self.assertEqual(response_list_after.status_code, 200)
        self.assertContains(
            response_list_after,
            Label.objects.get(name='old_label')
        )
        self.assertQuerysetEqual(
            response_list_after.context['object_list'],
            ['<Label: old_label>']
        )

    def test_delete_label(self):
        label_pk = Label.objects.get(name='new_label').pk
        url_list = reverse('tasks:labels_list')
        url_delete = reverse('tasks:delete_label', args=(label_pk,))
        response_list = self.client.get(url_list)
        self.assertEqual(response_list.status_code, 200)
        self.assertContains(response_list, Label.objects.get(name='new_label'))
        self.assertQuerysetEqual(
            response_list.context['object_list'],
            ['<Label: new_label>']
        )
        self.client.delete(url_delete, Label.objects.get(name='new_label'))
        response_list_after = self.client.get(url_list)
        self.assertEqual(response_list_after.status_code, 200)
        self.assertQuerysetEqual(
            response_list_after.context['object_list'],
            []
        )

    def test_create_label_within_form(self):
        url = reverse('tasks:create_label')
        response_from_create_form = self.client.get(url)
        self.assertEqual(response_from_create_form.status_code, 200)
        self.client.post(url, {'name': 'DANCE_LABEL'})
        response_after_create = self.client.get(reverse('tasks:labels_list'))
        self.assertEqual(response_after_create.status_code, 200)
        self.assertContains(
            response_after_create,
            Label.objects.get(name='DANCE_LABEL')
        )
