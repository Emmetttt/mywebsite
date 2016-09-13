import datetime
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Band(models.Model):
    band_name = models.CharField(max_length=50)
    def __str__(self):
        return self.question_text
