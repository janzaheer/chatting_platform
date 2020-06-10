from django import template

register = template.Library()


@register.simple_tag
def get_member_chat(room, user_id):
    return room.chat_member(user_id)
