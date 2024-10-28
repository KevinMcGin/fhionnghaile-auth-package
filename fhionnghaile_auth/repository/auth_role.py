from fhionnghaile_database.repository.database import db
from sqlalchemy.dialects.postgresql import UUID

class AuthRole(db.Model):
    __tablename__ = 'inf_auth_role'
    role = db.Column(db.String(100), primary_key=True)

    def __init__(
        self, 
        role,
    ):
        self.role = role
