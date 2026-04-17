from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class EmbedRecord(db.Model):
    __tablename__ = "embed_records"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(64), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    discriminator = db.Column(db.String(10), nullable=True)
    message_id = db.Column(db.String(64), nullable=False)
    channel_id = db.Column(db.String(64), nullable=False)
    embed_payload = db.Column(db.JSON, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<EmbedRecord {self.id} user={self.username}#{self.discriminator}>"
