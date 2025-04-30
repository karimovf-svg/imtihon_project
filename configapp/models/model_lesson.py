from django.db import models
from ..models import BaseModel, GroupStudent, Teacher

class Lesson(BaseModel):
    title = models.CharField(max_length=255)
    group = models.ForeignKey(GroupStudent, on_delete=models.CASCADE, related_name='lessons')
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, related_name='lessons')
    lesson_date = models.DateField()

    def __str__(self):
        return f"{self.title} - {self.group.title} - {self.lesson_date}"

    class Meta:
        verbose_name = 'Lesson'
        verbose_name_plural = 'Lessons'
        ordering = ['-lesson_date']
