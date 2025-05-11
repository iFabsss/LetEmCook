# accounts/signals.py
from allauth.account.signals import user_signed_up
from django.dispatch import receiver
import random

@receiver(user_signed_up)
def set_username_from_social_data(request, user, sociallogin=None, **kwargs):
    if sociallogin:
        provider = sociallogin.account.provider
        extra_data = sociallogin.account.extra_data

        if provider == 'google':
            # Google provides 'name', 'given_name', 'family_name'
            user.username = extra_data.get('name', user.username)

        elif provider == 'github':
            # GitHub provides 'login' as the username, 'name' as display name
            user.username = extra_data.get('login', user.username)

        else:
            user.username = generate_fallback_username(user)

        user.save()

def generate_fallback_username():
    return f"user{random.randint(1000, 9999)}"
