from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    description = models.TextField()
    # TODO: add picture


class Friendship(models.Model):
    from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)


# return friend id's no matter who send invitation
def get_friends(user):
    from_user = Friendship.objects.filter(from_user=user, accepted=True).values_list('to_user', flat=True)
    to_user = Friendship.objects.filter(to_user=user, accepted=True).values_list('from_user', flat=True)
    users_ids = set(from_user).union(to_user)
    return User.objects.filter(id__in=users_ids)
