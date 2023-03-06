from django.contrib.auth.models import User
from .models import Profile
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

# @receiver(post_save, sender=Profile)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name,
        )


def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    if created is False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()


# @receiver(post_delete, sender=Profile)
def delete_user(sender, instance, **kwargs):
    user = instance.user
    user.delete()


post_save.connect(create_profile, sender=User)
post_save.connect(updateUser, sender=Profile)
post_delete.connect(delete_user, sender=Profile)
