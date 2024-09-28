from fhionnghaile_database.repository.database import db
from datetime import datetime

class AnonymousUser(db.Model):
    __tablename__ = 'inf_anonymous_user'
    anonymous_user_id = db.Column(db.String(1000), primary_key=True)
    user_name = db.Column(db.String(100))
    created_on = db.Column(db.DateTime, default=db.func.current_timestamp())
    last_login = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(
        self, 
        anonymous_user_id,
        user_name,
        created_on = None,
        last_login = None
    ):
        self.anonymous_user_id = anonymous_user_id
        self.user_name = user_name
        self.created_on = created_on
        self.last_login = last_login

def save_anonymous_user(anonymous_user):
    db.session.add(anonymous_user)
    db.session.commit()
    return anonymous_user

def get_anonymous_user_by_anonymous_user_id(anonymous_user_id):
    return AnonymousUser.query \
        .filter_by(
            anonymous_user_id=anonymous_user_id
        ) \
        .first()

def get_anonymous_user_by_name(user_name):
    return AnonymousUser.query \
        .filter_by(
            user_name=user_name
        ) \
        .first()

def get_all_anonymous_users():
    return AnonymousUser.query.all()

def update_anonymous_user(anonymous_user_id, user):
    user_to_update = get_anonymous_user_by_anonymous_user_id(anonymous_user_id)
    user_to_update.user_name = user.user_name
    user_to_update.last_login = user.last_login

    db.session.commit()
    return user_to_update

def delete_anonymous_user(anonymous_user_id):
    user = get_anonymous_user_by_anonymous_user_id(anonymous_user_id)
    db.session.delete(user)
    db.session.commit()
    return user

def login_anonymous_user(anonymous_user_id):
    user = get_anonymous_user_by_anonymous_user_id(anonymous_user_id)
    user.last_login = datetime.now()
    db.session.commit()
    return user