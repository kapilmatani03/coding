from functools import wraps

from app.extensions import db


def session_manager(commit=False):
    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                r_val = func(*args, **kwargs)
                if commit:
                    db.session.commit()
                return r_val
            except:
                db.session.rollback()
                raise

            finally:
                db.session.remove()

        return wrapper

    return decorator
