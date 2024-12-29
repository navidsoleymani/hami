from django.db import models


# Create your models here.
# class TelegramUser(models.Model):
#     user_id = models.CharField(max_length=255, unique=True)
#     name = models.CharField(max_length=255)
#
#     def __str__(self):
#         return f"{self.user_id} ({self.user_id})"


# class InstagramUser(models.Model):
#     user_id = models.CharField(max_length=255)
#     telegram_user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return f"{self.user_id} ({self.telegram_user})"


class Goal(models.Model):
    """
    telegram user goals
    """
    user_id = models.CharField(max_length=255)
    follower_count = models.IntegerField(default=0)
    telegram_user = models.CharField(max_length=255)


class FollowerCount(models.Model):
    """
    for historical use only
    """
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE)
    followers = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.goal}"
