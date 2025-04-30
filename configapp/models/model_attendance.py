from django.db import models
from ..models import Student, GroupStudent, BaseModel

class Status(BaseModel):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Status'
        verbose_name_plural = 'Statuses'


class Attendance(BaseModel):
    group = models.ForeignKey(GroupStudent, on_delete=models.CASCADE, related_name='group_attendance')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_attendance')
    lesson = models.ForeignKey('configapp.Lesson', on_delete=models.CASCADE, related_name='lesson_attendances')
    is_status = models.ForeignKey('Status', on_delete=models.CASCADE, related_name='is_status')

    def __str__(self):
        return f"{self.student.user.phone_number} - {self.group.title}"

    class Meta:
        verbose_name = "Attendance"
        verbose_name_plural = "Attendances"