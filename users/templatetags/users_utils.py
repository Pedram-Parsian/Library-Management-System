from django import template
from users.models import User

register = template.Library()


@register.simple_tag
def get_avatar_with_size(user, size):
    user: User
    return user.get_avatar(size)
