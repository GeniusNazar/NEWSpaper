from django.db import models
from django.contrib.auth.models import User


class Article(models.Model):

    STATUS_CHOICES = [
        ("Чернетка", "Чернетка"),
        ("Опубліковано", "Опубліковано"),
    ]

    CATEGORY_CHOICES = [
        ("Технології", "Технології"),
        ("Кухня", "Кухня"),
        ("Навчання", "Навчання")
    ]

    title = models.CharField(max_length=256)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="published")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="studying")
    due_date = models.DateField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")

    def __str__(self):
        return self.title


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    media = models.FileField(upload_to="comments_new/", blank=True, null=True)

    def get_absolute_url(self):
        return self.article.get_absolute_url()