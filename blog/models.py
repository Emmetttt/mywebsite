from django.db import models
from django.utils import timezone


class Post(models.Model): #model saved in database
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200) #limited no characters
    text = models.TextField() #unlimited numbers characters
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self): #we will get a string
        return self.title
