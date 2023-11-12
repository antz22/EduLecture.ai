from django.contrib.auth.models import AbstractUser
from django.db import models

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return "user_{0}/{1}".format(instance.id, filename)  

class User(AbstractUser):
    name = models.CharField(max_length=64, null=True, blank=True)
    voice_id = models.CharField(max_length=256, null=True, blank=True)
    voice_file = models.FileField(upload_to=user_directory_path, null=True, blank=True)

class Subject(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Lecture(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lectures')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=64, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    presentation_link = models.CharField(max_length=256, null=True, blank=True)
    video_link = models.CharField(max_length=256, null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.title + " - " + self.user.name
