from functools import wraps
from flask import request, g
from models import Account
from session import session

def check_auth(email, password):
    account = session.query(Account).filter(Account.email == email).first()
    if account and account.verify_password(password):
        g.account = account
        return True
    else:
        return False

def authenticate():
    return ('Could not verify your access level', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_user_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return wrapper

def requires_admin_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password) or not g.account.admin:
            return authenticate()
        return f(*args, **kwargs)
    return wrapper


def requires_keg_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        f(*args, **kwargs)
    return decorated
