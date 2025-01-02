from django.db import models
from .utils.db import BaseDBModel

class Goal(BaseDBModel):
    """
    telegram user goals
    """
    user_id = models.CharField(max_length=255)
    follower_count = models.IntegerField(default=0)
    telegram_user = models.CharField(max_length=255)


class FollowerCount(BaseDBModel):
    """
    for historical use only
    """
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE)
    followers = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.goal}"
