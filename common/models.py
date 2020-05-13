from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.db.models.signals import post_save
from chat. models import Room

class UserProfile(models.Model):
    USER_TYPE_USER = 'user'
    USER_TYPE_PAGE_ADMIN = 'page_admin'
    USER_TYPE_OWNER = 'owner'
    USER_TYPE_MEMBER = 'member'

    USER_TYPES = (
        (USER_TYPE_USER, 'user'),
        (USER_TYPE_PAGE_ADMIN, 'page_admin'),
        (USER_TYPE_OWNER, 'owner'),
        (USER_TYPE_MEMBER, 'member'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='user_profile')
    company_name = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    profile_name = models.CharField(max_length=256, blank=True, null=True)
    profile_image = models.ImageField(upload_to="customer/profile/", null=True, blank=True)
    is_custom_profile_image = models.BooleanField(default=False)
    phone = models.CharField(max_length=256, blank=True, null=True)
    alternate_phone = models.CharField(max_length=256, blank=True, null=True)
    gender = models.CharField(
        max_length=1, choices=(('m', _('Male')), ('f', _('Female'))),
        blank=True, null=True)
    type = models.CharField(
        max_length=200, choices=USER_TYPES, default=USER_TYPE_USER,
        blank=True, null=True)
    hometown = models.CharField(max_length=256, blank=True, null=True)
    company_name = models.CharField(max_length=256, blank=True, null=True)
    location = models.CharField(max_length=256, blank=True, null=True)
    address = models.CharField(max_length=256, blank=True, null=True)

    def __unicode__(self):
        return self.user.username


def create_profile(sender, instance, created, **kwargs):
    """
    The functions used to check if user profile is not created
    and created the user profile without saving role and hospital
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    if created and not UserProfile.objects.filter(user=instance):
        return UserProfile.objects.create(
            user=instance
        )


# Signals
post_save.connect(create_profile, sender=User)

class MemberChatRoom(models.Model):
    CHAT_TYPE_REQUESTED = 'requested'
    CHAT_TYPE_APPROVED = 'approved'
    CHAT_TYPE_CANCLE = 'cancle'

    CHAT_TYPES = (
        (CHAT_TYPE_REQUESTED, 'requested'),
        (CHAT_TYPE_APPROVED, 'approved'),
        (CHAT_TYPE_CANCLE, 'cancle'),
    )

    user = models.ManyToManyField(User, related_name='user_member_chat_room',max_length=100
    )
    room = models.ManyToManyField(Room, related_name='room_member_chat_room',max_length=100
    )
    status = models.CharField(
        max_length=200, choices=CHAT_TYPES, default=CHAT_TYPE_CANCLE,
        blank=True, null=True)

    def __unicode__(self):
        return self.user.username

