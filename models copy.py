from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime



class User(AbstractUser,models.Model):
    following=models.ManyToManyField('self',blank=True,symmetrical=False,related_name='followers')
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username           
            
        }


class Posts(models.Model):
    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name="posts")
    content=models.TextField()
    liker=models.ManyToManyField(User,blank=True,related_name='liked')
    timestamp=models.DateTimeField(default=datetime.datetime.now())
    likes=models.IntegerField(default=0)

    def serialize(self):
        return {
            "id": self.id,
            "owner": self.owner.serialize(),
            "likes":self.likes,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p")
            
        }


