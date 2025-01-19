from flask import redirect
from flask_login import current_user


def admin_required(func):
    def wrapper(*args, **kwargs):
        if current_user.role != 'Admin':
            return redirect("/catalogue")
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

def no_admin_required(func):
    def wrapper(*args, **kwargs):
        if current_user.role == 'Admin':
            return redirect("/")
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper
