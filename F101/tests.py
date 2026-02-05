# F101/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from .models import Student

# Test Model


class StudentModelTest(TestCase):

    def test_create_student(self):
        student = Student.objects.create(name="John", age=20)
        self.assertEqual(student.name, "John")
        self.assertEqual(student.age, 20)
        self.assertEqual(str(student), "John")

    def test_student_count(self):
        Student.objects.create(name="Alice", age=22)
        Student.objects.create(name="Bob", age=23)
        self.assertEqual(Student.objects.count(), 2)

# Test View


class HomeViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"HOME PAGE", response.content)


class StudentListViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        Student.objects.create(name="Test1", age=18)
        Student.objects.create(name="Test2", age=19)

    def test_student_list_view(self):
        response = self.client.get(reverse('student_list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Test1", response.content)
        self.assertIn(b"Test2", response.content)


class StudentDetailViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.student = Student.objects.create(name="Detail", age=25)

    def test_student_detail_view(self):
        response = self.client.get(reverse('student_detail', args=[self.student.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Detail", response.content)
        self.assertIn(b"25", response.content)

    def test_student_detail_404(self):
        response = self.client.get(reverse('student_detail', args=[999]))
        self.assertEqual(response.status_code, 404)


class APIViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        Student.objects.create(name="API", age=30)

    def test_api_students(self):
        response = self.client.get(reverse('api_students'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

        # Check JSON data
        import json
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], 'API')
        self.assertEqual(data[0]['age'], 30)

# Integration Test


class IntegrationTest(TestCase):

    def test_full_flow(self):
        # 1. Truy cập home
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

        # 2. Tạo student
        student = Student.objects.create(name="Flow", age=21)

        # 3. Truy cập danh sách
        response = self.client.get(reverse('student_list'))
        self.assertIn(b"Flow", response.content)

        # 4. Truy cập chi tiết
        response = self.client.get(reverse('student_detail', args=[student.id]))
        self.assertIn(b"21", response.content)

        # 5. Truy cập API
        response = self.client.get(reverse('api_students'))
        self.assertEqual(response.status_code, 200)
