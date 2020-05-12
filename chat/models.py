from django.db import models
from django.contrib.auth.models import User


class Room(models.Model):
    """
    A room for people to chat in.
    """

    # Room title
    title = models.CharField(max_length=255)

    # If only "staff" users are allowed (is_staff on django's User)
    staff_only = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    @property
    def group_name(self):
        """
        Returns the Channels Group name that sockets should subscribe to to get sent
        messages as they are generated.
        """
        return "room-%s" % self.id

class RoomAdmin(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE,
     related_name='admin_room', blank=True, null=True
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE,
     related_name='user_room_admin', blank=True, null=True
    )
    status=models.BooleanField(default=True)

    def __str__(self):
        return self.room.title
