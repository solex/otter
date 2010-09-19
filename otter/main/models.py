from django.db import models
from django.contrib.auth.models import User as BaseUser


class User(BaseUser):
    
    class Meta:
        proxy = True

    def public_messages(self):
        return self.messages_sent.filter(to_user__isnull = True, 
                                         to_team__isnull = True)

class Team(models.Model):
    
    name = models.CharField(max_length=255)
    users = models.ManyToManyField(User)

#TODO: Task


class Message(models.Model):

    #TODO: Update meassages with MC client

    sender = models.ForeignKey(User, related_name='messages_sent')
    text = models.TextField()
    to_user = models.ForeignKey(User, blank=True, null=True,
                                related_name='messages_received')
    to_team = models.ForeignKey(Team, blank=True, null=True)

    #TODO: tags, priority, mentioned

