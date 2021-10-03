from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Notes(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        verbose_name = "notes"
        verbose_name_plural = "Notes"
    def __str__(self):
        return self.title


class Homework(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    description = models.TextField()
    due = models.DateTimeField()
    finished = models.BooleanField(default=False)


    class Meta:
        verbose_name = "homework"
        verbose_name_plural = "HomeWork"
    def __str__(self):
        return self.title


class Todo(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    finished = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Todo"
        verbose_name_plural = "To Do"
    def __str__(self):
        return self.title