from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
import uuid


class MyUserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        user = self.model(username=username,full_name=extra_fields.get('full_name'),teacher_id=extra_fields.get('teacher_id'),year_of_birth=extra_fields.get('year_of_birth'),phone = username, degree = extra_fields.get('degree'),salary_per_hour= extra_fields.get('salary_per_hour'), location = extra_fields.get('location'))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone, password, **extra_fields):

        user = self.model(username=phone, full_name='',
                          teacher_id=uuid.uuid4(), year_of_birth=2000,
                          phone=phone, degree=1.3,
                          salary_per_hour=1000, location= '',is_superuser=True,is_staff=True)
        user.set_password(password)
        user.save()
        return user

        # return self.create_user(phone, password, **extra_fields)

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
    REQUIRED_FIELDS = []

    objects = MyUserManager()

    def __str__(self):
        return str(self.phone) + '-' + str(self.full_name)

class Subject(models.Model):
    subject_name = models.CharField(max_length=100, null=False,blank=False)
    subject_factor =  models.FloatField(default=0)
    subject_id = models.AutoField(primary_key=True,auto_created=True)
    def __str__(self):
        return self.subject_name

    objects = models.Manager()


class Class(models.Model):
    class_id = models.CharField(max_length=10, null=False,unique=True)
    class_name = models.CharField(max_length=100, null=False,blank=False)
    class_factor = models.FloatField(default=0)
    number_of_lessons = models.IntegerField(default=1)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, default=1)

    def __str__(self):
        return self.class_name

    objects = models.Manager()


