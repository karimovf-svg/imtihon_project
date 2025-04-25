from django.db import models
from ..models import BaseModel, Course, GroupStudent, Teacher, Student

class Homework(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    group = models.ForeignKey(GroupStudent, on_delete=models.CASCADE, related_name='homeworks')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='homeworks')

    def __str__(self):
        return f"{self.title} - {self.group.title}"

    class Meta:
        verbose_name = 'Homework'
        verbose_name_plural = 'Homeworks'

class HomeworkSubmission(BaseModel):
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='submissions')
    link = models.CharField(max_length=255)
    is_checked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.user.phone_number} - {self.homework.title}"

    verbose_name = 'Homework Submission'
    verbose_name_plural = 'Homework Submissions'

class HomeworkReview(BaseModel):
    submission = models.OneToOneField(HomeworkSubmission, on_delete=models.CASCADE, related_name='review')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='reviews')
    comment = models.TextField(null=True, blank=True)
    ball = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"Review for {self.submission.student.user.phone_number} - {self.submission.homework.title}"