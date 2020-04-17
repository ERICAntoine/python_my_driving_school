from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

class UserManager(BaseUserManager):
    def create_user(self, firstname, lastname, email, password, role):

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            firstname= firstname,
            lastname=lastname,
            email=self.normalize_email(email),
            role=role,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

# Create your models here.

class Role(models.Model):
    name = models.CharField(max_length = 20)
    
    def __str__(self):
        return self.name

class Users(AbstractBaseUser):
    firstname = models.CharField(max_length = 40)
    lastname = models.CharField(max_length = 40)
    email = models.EmailField(max_length = 254, unique=True)
    password = models.CharField(max_length=100)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="right")
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Email & Password are required by default.

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active


class Planning(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    instructor = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="instructor")
    student = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="student")
    title = models.CharField(max_length=100)

class Plan(models.Model):
    hour = models.CharField(max_length = 20)

class LinkPlanUsers(models.Model):
    student = models.ForeignKey(Users, on_delete=models.CASCADE)
    hour = models.ForeignKey(Plan, on_delete=models.CASCADE)
