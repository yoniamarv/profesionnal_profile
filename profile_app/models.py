from django.db import models
from django.contrib.auth.models import User


class City(models.Model):
  name = models.CharField(max_length=264, default='')

  def __str__(self):
    return self.name


class Gender(models.Model):
  name = models.CharField(max_length=264, default='')

  def __str__(self):
    return self.name


class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  bio = models.TextField()
  city = models.ForeignKey(City, on_delete=models.CASCADE, blank=True, default=0)
  gender = models.ForeignKey(Gender, on_delete=models.CASCADE, blank=True, default=0)

  def __str__(self):
    return self.user.username
