from django.db import models

# Create your models here.
class signin(models.Model):
    username=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    password=models.CharField(max_length=50)
    otp=models.CharField(max_length=10)
    is_verified=models.IntegerField()

class operation(models.Model):
    def __str__(self):
        return self.user_id
    long_url=models.CharField(max_length=500)
    short_url=models.CharField(max_length=100)
    user_id=models.CharField(max_length=100,default=0)