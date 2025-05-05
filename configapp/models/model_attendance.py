from django.db import models
from ..models import Student, GroupStudent, BaseModel

class Attendance(BaseModel):
    class StatusChoices(models.TextChoices):
        KELDI = 'keldi', 'Keldi'
        KELMADI = 'kelmadi', 'Kelmadi'
        KECHIKDI = 'kechikdi', 'Kechikdi'
        SABABLI = 'sababli', 'Sababli'

    group = models.ForeignKey(GroupStudent, on_delete=models.CASCADE, related_name='group_attendance')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_attendance')
    lesson = models.ForeignKey('configapp.Lesson', on_delete=models.CASCADE, related_name='lesson_attendances')
    is_status = models.CharField(max_length=10, choices=StatusChoices.choices)

    def __str__(self):
        return f"{self.student.user.phone_number} - {self.group.title} - - {self.is_status}"

    class Meta:
        verbose_name = "Attendance"
        verbose_name_plural = "Attendances"