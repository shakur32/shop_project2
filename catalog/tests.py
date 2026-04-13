from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Task

class TaskAPITests(APITestCase):
    def setUp(self):
        # Создаем двух пользователей для тестов
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')
        
        # Ссылка на регистрацию и логин
        self.register_url = '/api/register/'
        self.login_url = '/api/login/'
        self.tasks_url = '/api/tasks/'

    def test_registration(self):
        """Тест регистрации пользователя"""
        data = {"username": "newuser", "password": "newpassword123", "email": "new@test.com"}
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_and_create_task(self):
        """Тест входа и создания задачи"""
        # Логинимся (получаем JWT токен)
        login_response = self.client.post(self.login_url, {"username": "user1", "password": "password123"})
        token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        
        # Создаем задачу
        data = {"title": "Test Task", "status": "new", "priority": "medium"}
        response = self.client.post(self.tasks_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().owner, self.user1)

    def test_access_denied_for_other_user(self):
        """Запрет доступа к чужой задаче"""
        # Создаем задачу от имени user1
        task = Task.objects.create(title="User1 Task", owner=self.user1)
        
        # Логинимся под user2
        login_response = self.client.post(self.login_url, {"username": "user2", "password": "password123"})
        token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        
        # Пытаемся получить список (задача user1 не должна там появиться)
        response = self.client.get(self.tasks_url)
        self.assertEqual(len(response.data['results']), 0)