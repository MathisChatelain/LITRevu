from authentication.models import User
from .models import Ticket, Review


def unlazy_user(request_user):
    """Get the user object from the request"""
    return request_user._wrapped if hasattr(request_user, "_wrapped") else request_user


def get_current_user(request_user: User):
    """Get the user object from the request"""
    return User.objects.get(username=unlazy_user(request_user))


def get_users_viewable_for_model(request_user: User, model: Ticket | Review):
    """Get all reviews from users that the current user follows"""
    user = unlazy_user(request_user)
    return (
        model.objects.filter(user__in=user.user_follows.all())
        if hasattr(user, "user_follows")
        else model.objects.none()
    ) | model.objects.filter(user=user)
