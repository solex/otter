from django.db import models
from django.contrib.auth.models import User as BaseUser


class User(BaseUser):
    
    class Meta:
        proxy = True

    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)

    @property
    def odesk_id(self):
        return self.username.split('@')[0]


class Team(models.Model):
    
    title = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    users = models.ManyToManyField(User)

    def __unicode__(self):
        return self.title

#TODO: Task


class Message(models.Model):

    #TODO: Update messages with MC client

    sender = models.ForeignKey(User, related_name='messages_sent')
    text = models.TextField()
    to_user = models.ForeignKey(User, blank=True, null=True,
                                related_name='messages_received')
    to_team = models.ForeignKey(Team, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    #TODO: tags, priority, mentioned

class FavTeam(models.Model):
    
    user = models.ForeignKey(User)
    team = models.ForeignKey(Team)

class FavUser(models.Model):
    
    user = models.ForeignKey(User, related_name='following')
    follow = models.ForeignKey(User, related_name='followers')
