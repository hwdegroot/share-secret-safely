from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from wsgi_app import db


class Secret(db.Model):
    __tablename__ = 'secrets'

    id = db.Column(UUID(as_uuid=True), primary_key=True)
    password_hash = db.Column(db.Text, nullable=True)
    ttl = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    def __init__(self, password_hash, ttl=None):
        self.id = uuid.uuid4()
        self.password_hash = password_hash
        self.ttl = None

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str({
            "id": self.id,
            "password_hash": self.password_hash,
            "ttl": self.ttl,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        })
