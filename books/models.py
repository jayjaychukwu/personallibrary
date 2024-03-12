from django.contrib.auth import get_user_model
from django.db import models

from utils.models.helpers import BaseModel


class Book(BaseModel):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    ISBN = models.CharField(max_length=15)
    publication_date = models.DateField()

    def __str__(self):
        return f"{self.title} by {self.author}"
