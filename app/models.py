from django.db import models
from django.contrib.auth.models import User
from django.db.models import JSONField;

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    body = models.TextField()
    date = models.DateTimeField()
    upvotes = models.IntegerField(default = 0)
    downvotes = models.IntegerField(default = 0)
    voters = JSONField(default=dict);

    def set_user_vote(self, user, vote_type):
        self.voters[user.username] = vote_type
        self.save()

    def get_user_vote(self, user):
        return self.voters.get(user.username, None)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    date = models.DateTimeField()
    upvotes = models.IntegerField(default = 0)
    downvotes = models.IntegerField(default = 0)
    voters = JSONField(default=dict);

    def set_user_vote(self, user, vote_type):
        self.voters[user.username] = vote_type
        self.save()

    def get_user_vote(self, user):
        return self.voters.get(user.username, None)
