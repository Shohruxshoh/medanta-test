from django.db import models
from user.models import User


# Create your models here.

class BaseModel(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)


class CardUser(BaseModel, models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_number = models.IntegerField(default=0)
    card_mm = models.IntegerField(default=0)
    card_yy = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.last_name} {self.card_number}"


class Post(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Post1(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title
