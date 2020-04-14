from django.db import models

# Create your models here.

class Role(models.Model):
    name = models.CharField(max_length = 20)
    
    def __str__(self):
        return self.name

class Users(models.Model):
    firstname = models.CharField(max_length = 40)
    lastname = models.CharField(max_length = 40)
    email = models.EmailField(max_length = 254)
    password = models.CharField(max_length=100)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="right")

    def __str__(self): 
        return self.email


class Planning(models.Model):
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    instructor = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="instructor")
    student = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="student")


