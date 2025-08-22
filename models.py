# models.py
from datetime import datetime
from app import db  # safe because app imports this file ONLY after db.init_app()

class User(db.Model):
    __tablename__ = 'users'

    # MUST have a primary key:
    id = db.Column(db.Integer, primary_key=True)

    # DB column name is literally 'user' (per your spec),
    # Python attribute is 'username' to avoid reserved-word collisions in code.
    username = db.Column('user', db.String(80), unique=True, nullable=False)

    password_hash = db.Column(db.String(255), nullable=False)
    dosha = db.Column(db.String(20), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    def to_dict(self):
        return {
            'id': self.id,
            'user': self.username,
            'dosha': self.dosha,
            'created_at': self.created_at.isoformat() + 'Z' if self.created_at else None,
            'updated_at': self.updated_at.isoformat() + 'Z' if self.updated_at else None,
        }

    def __repr__(self):
        return f"<User id={self.id} user={self.username!r}>"
