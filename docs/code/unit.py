# -*- coding: utf-8 -*-

"""app.bl.user"""

from app.bl import mail
from app.tasks.friendship import discover_possible_friends
from app.models import User
from app.utils.security import not_md5_and_has_salt


def create_user(email, password, full_name):
    user = User(email=email,
                password=not_md5_and_has_salt(password),
                full_name=full_name)
    user.save()
    score = count_score(user)
    if score < 10:
        choose_low_quality_avatar(user)
    else:
        choose_high_quality_avatar(user)
        mail.send_welcome_email(user)
        discover_possible_friends(user)
    return user


def count_score(user):
    pass


def choose_low_quality_avatar(user):
    pass


def choose_high_quality_avatar(user):
    pass
