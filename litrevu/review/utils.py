from authentication.models import User
from .models import Ticket, Review


def get_users_viewable_reviews(request_user: User):
    """Get all reviews from users that the current user follows"""
    user = request_user._wrapped if hasattr(request_user, "_wrapped") else request_user
    print(user.__dict__)
    return (
        Review.objects.filter(user__in=user.user_follows.all())
        if hasattr(user, "user_follows")
        else Review.objects.none()
    ) | Review.objects.filter(user=user)


def get_users_viewable_tickets(request_user: User):
    """Get all tickets from users that the current user follows"""
    user = request_user._wrapped if hasattr(request_user, "_wrapped") else request_user
    return (
        Ticket.objects.filter(user__in=user.user_follows.all())
        if hasattr(user, "user_follows")
        else Ticket.objects.none()
    ) | Ticket.objects.filter(user=user)
