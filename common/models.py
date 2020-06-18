from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.db.models.signals import post_save
from chat.models import Room
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class MessageModel(models.Model):
    """
    This class represents a chat message. It has a owner (user), timestamp and
    the message body.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user',
                      related_name='from_user', db_index=True)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='recipient',
                           related_name='to_user', db_index=True)
    timestamp = models.DateTimeField('timestamp', auto_now_add=True, editable=False,
                              db_index=True)
    body = models.TextField('body')

    def __str__(self):
        return str(self.id)

    def characters(self):
        """
        Toy function to count body characters.
        :return: body's char number
        """
        return len(self.body)

    def notify_ws_clients(self):
        """
        Inform client there is a new message.
        """
        notification = {
            'type': 'recieve_group_message',
            'message': '{}'.format(self.id)
        }

        channel_layer = get_channel_layer()
        print("user.id {}".format(self.user.id))
        print("user.id {}".format(self.recipient.id))

        async_to_sync(channel_layer.group_send)("{}".format(self.user.id), notification)
        async_to_sync(channel_layer.group_send)("{}".format(self.recipient.id), notification)

    def save(self, *args, **kwargs):
        """
        Trims white spaces, saves the message and notifies the recipient via WS
        if the message is new.
        """
        new = self.id
        self.body = self.body.strip()  # Trimming whitespaces from the body
        super(MessageModel, self).save(*args, **kwargs)
        if new is None:
            self.notify_ws_clients()


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

    STATUS_ONLINE = 'Online'
    STATUS_OFFLINE = 'Offline'
    STATUS_AWAY = 'Away'
    STATUS_DONT_DISTURB = 'Do not Disturb'

    STATUSES = (
        (STATUS_ONLINE, 'Online'),
        (STATUS_OFFLINE, 'Offline'),
        (STATUS_AWAY, 'Away'),
        (STATUS_DONT_DISTURB, 'Do not Disturb')
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
    status = models.CharField(max_length=100, choices=STATUSES,
                             default=STATUS_ONLINE, blank=True, null=True)

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
    CHAT_TYPE_CANCLE = 'cancel'

    CHAT_TYPES = (
        (CHAT_TYPE_REQUESTED, 'requested'),
        (CHAT_TYPE_APPROVED, 'approved'),
        (CHAT_TYPE_CANCLE, 'cancel'),
    )

    user = models.ForeignKey(User, related_name='user_member_chat_room',
                             on_delete=models.CASCADE)
    room = models.ForeignKey(Room, related_name='room_member_chat_room',
                             max_length=100, on_delete=models.CASCADE,
                             blank=True,null=True
    )
    status = models.CharField(
        max_length=200, choices=CHAT_TYPES, default=CHAT_TYPE_CANCLE,
        blank=True, null=True)

    def __unicode__(self):
        return self.user.username

