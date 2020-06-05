from django.contrib import admin
from .models import Room, RoomAdmin, PublicRoom, Comment


admin.site.register(
    Room,
    list_display=["id", "title", "staff_only"],
    list_display_links=["id", "title"],
)
admin.site.register(RoomAdmin)
admin.site.register(PublicRoom)
admin.site.register(Comment)
