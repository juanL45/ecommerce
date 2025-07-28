from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    bio = models.CharField(max_length=100,default="")
    USERNAME_FIELD ='email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.RESTRICT,null=True,blank=True)
    image=models.ImageField(upload_to="image",null=True,blank=True)
    full_name=models.CharField(max_length=255,null=True,blank=True)
    bio=models.CharField(max_length=255,null=True,blank=True)
    phone = models.CharField(max_length=255,null=True,blank=True)
    address = models.CharField(max_length=255,null=True,blank=True)
    country = models.CharField(max_length=255,null=True,blank=True)
    verified = models.BooleanField(default=False)
    def __str__(self):
        return self.user.username

class ContactUs(models.Model):
    full_name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    phone=models.CharField(max_length=255)
    subject=models.CharField(max_length=255)
    message=models.TextField()
    
    class Meta:
        verbose_name = "Contactanos"
        verbose_name_plural = "Contactanos"
    def __str__(self):
        return self.full_name
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)
def save_user_profile(sender,instance,**kwargs):
    instance.profile.save()
post_save.connect(create_user_profile,sender=User)
post_save.connect(save_user_profile,sender=User)