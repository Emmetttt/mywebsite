from django.db import models
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField 



class Post(models.Model): #model saved in database
    author = models.ForeignKey('auth.User', on_delete=models.PROTECT)
    title = models.CharField(max_length=200) #limited no characters
    description = models.CharField(max_length=400) #limited no characters
    text = RichTextUploadingField() #unlimited numbers characters
    tag = models.CharField(max_length=50)
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self): #we will get a string
        return self.title

