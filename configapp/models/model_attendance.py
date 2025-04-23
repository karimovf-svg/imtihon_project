from django.db import models
from ..models import Student, GroupStudent

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    group = models.ForeignKey(GroupStudent, on_delete=models.CASCADE)
    is_status = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.group} - {'Keldi' if self.is_status else 'kelmadi'}"
