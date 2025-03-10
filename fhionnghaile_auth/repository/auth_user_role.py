from fhionnghaile_database.repository.database import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class AuthUserRole(db.Model):
    __tablename__ = 'inf_auth_user_role'
    auth_user_role_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    auth_role = db.Column(db.String(100), db.ForeignKey('inf_auth_role.auth_role'))
    auth_user_id = db.Column(db.String(1000), db.ForeignKey('inf_auth_user.auth_user_id'))

    def __init__(
        self, 
        auth_user_role_id,
        auth_role,
        auth_user_id,
    ):
        self.auth_user_role_id = auth_user_role_id
        self.auth_role = auth_role
        self.auth_user_id = auth_user_id 

def get_roles_by_user_id(auth_user_id):
    return db.session.query(
        AuthUserRole.auth_role
    ).filter_by(
        auth_user_id=auth_user_id
    ).all()