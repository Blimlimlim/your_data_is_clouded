# import auth module
from firebase_admin import auth


def register_new_user(display_name, email, password):
    """ 
    Creates a new user in firebase using strings for email and password.
    Reports success. Returns the new user's uid 
    """
    user = auth.create_user(display_name = display_name, email = email, password = password)
    # print(f"user created success. UID: {user.uid}")
    return user

def get_user(email):
    """returns the user with the provided email"""
    return auth.get_user_by_email(email)

def get_uid(user):
    """
    Returns the uid associated with an existing user.
    Useful for log in
    """
    return user.uid

def get_display_name(user):
    """Returns the display_name of an existing user."""
    return user.display_name