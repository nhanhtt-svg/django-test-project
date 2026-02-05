# F101/views.py
from django.http import HttpResponse, JsonResponse
from .models import Student

# Không dùng template, chỉ return HttpResponse đơn giản


def home(request):
    return HttpResponse("HOME PAGE")


def student_list(request):
    students = Student.objects.all()
    result = "<h1>Student List</h1><ul>"
    for student in students:
        result += f"<li>{student.name} - {student.age} tuổi</li>"
    result += "</ul>"
    return HttpResponse(result)


def student_detail(request, student_id):
    try:
        student = Student.objects.get(id=student_id)
        return HttpResponse(f"<h1>Student Detail</h1><p>Name: {student.name}</p><p>Age: {student.age}</p>")
    except Student.DoesNotExist:
        return HttpResponse("Student not found", status=404)


def api_students(request):
    students = list(Student.objects.values('id', 'name', 'age'))
    return JsonResponse(students, safe=False)
