from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
import uuid


PRIORITIES = (
    (1.3, 'Tốt nghiệp đại học'),
    (1.4, 'Thạc sỹ'),
    (1.5, 'Tiến sỹ'),
    (1.6, 'Phó giáo sư'),
    (1.7, 'Giáo sư')
)

class User(AbstractUser):
    full_name = models.CharField(max_length=200, null=False)
    teacher_id = models.CharField(max_length=6, null=False,unique=True)
    year_of_birth = models.IntegerField(null=False,blank=False)
    phone = models.CharField(max_length=10, null=False,unique=True )
    degree = models.FloatField(default=1.3, choices=PRIORITIES)
    salary_per_hour = models.IntegerField(default=100000)
    location = models.CharField(max_length=250,null=False,blank=False)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['username']


    def __str__(self):
        return str(self.phone) + '-' + str(self.full_name)


class Class(models.Model):
    class_id = models.CharField(max_length=5, null=False,unique=True)
    class_name = models.CharField(max_length=100, null=False,blank=False)
    class_factor = models.FloatField(default=0)
    subject_factor =  models.FloatField(default=0)
    number_of_lessons = models.IntegerField(default=1)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.class_name

    objects = models.Manager()


