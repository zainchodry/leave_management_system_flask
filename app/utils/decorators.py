from functools import wraps

from flask import (
    abort
)

from flask_login import (
    current_user
)

def admin_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        if (
            not current_user.is_authenticated
            or current_user.role != "ADMIN"
        ):
            abort(403)

        return func(
            *args,
            **kwargs
        )

    return wrapper

def teacher_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        if (
            not current_user.is_authenticated
            or current_user.role != "TEACHER"
        ):
            abort(403)

        return func(
            *args,
            **kwargs
        )

    return wrapper

def student_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        if (
            not current_user.is_authenticated
            or current_user.role != "STUDENT"
        ):
            abort(403)

        return func(
            *args,
            **kwargs
        )

    return wrapper
