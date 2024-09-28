from fhionnghaile.auth.repository.database import db
from datetime import datetime

class AuthUser(db.Model):
    __tablename__ = 'inf_auth_user'
    auth_user_id = db.Column(db.String(1000), primary_key=True)
    email = db.Column(db.String(320))
    user_name = db.Column(db.String(100))
    created_on = db.Column(db.DateTime, default=db.func.current_timestamp())
    last_login = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(
        self, 
        auth_user_id,
        email,
        user_name,
        created_on = None,
        last_login = None
    ):
        self.auth_user_id = auth_user_id
        self.email = email
        self.user_name = user_name
        self.created_on = created_on
        self.last_login = last_login

def save_auth_user(auth_user):
    db.session.add(auth_user)
    db.session.commit()
    return auth_user

def get_auth_user_by_auth_user_id(auth_user_id):
    return AuthUser.query \
        .filter_by(
            auth_user_id=auth_user_id
        ) \
        .first()

def get_auth_user_by_name(user_name):
    return AuthUser.query \
        .filter_by(
            user_name=user_name
        ) \
        .first()

def get_auth_user_by_email(email):
    return AuthUser.query \
        .filter_by(
            email=email
        ) \
        .first()

def get_all_auth_users():
    return AuthUser.query.all()

def update_auth_user(email, user):
    user_to_update = get_auth_user_by_email(email)
    user_to_update.email = user.email
    user_to_update.user_name = user.user_name
    user_to_update.last_login = user.last_login

    db.session.commit()
    return user_to_update

def delete_auth_user(auth_user_id):
    user = get_auth_user_by_auth_user_id(auth_user_id)
    db.session.delete(user)
    db.session.commit()
    return user

def login_auth_user(email):
    user = get_auth_user_by_email(email)
    user.last_login = datetime.now()
    db.session.commit()
    return user