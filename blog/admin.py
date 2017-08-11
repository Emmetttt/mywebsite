from django.contrib import admin
from .models import Post
from django.forms import ModelForm
from django.contrib.admin import ModelAdmin
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class PostForm(ModelForm):
    class Meta:
        model = Post
        widgets = {
            'text': CKEditorUploadingWidget()
        }
        fields = '__all__'

class PostAdmin(ModelAdmin):
    form = PostForm

admin.site.register(Post, PostAdmin)


