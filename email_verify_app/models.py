from django.db import models
from django.contrib.auth.models import AbstractUser,UserManager

class User(AbstractUser):
    objects = UserManager()
    email = models.EmailField(("email address"), blank=False)
    
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=200)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username

