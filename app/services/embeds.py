from ..db import db, EmbedRecord
from datetime import datetime


def save_embed_record(user, payload, message_id, channel_id):
    record = EmbedRecord(
        user_id=user["id"],
        username=user.get("username", "unknown"),
        discriminator=user.get("discriminator"),
        message_id=message_id,
        channel_id=channel_id,
        embed_payload=payload,
    )
    db.session.add(record)
    db.session.commit()
    return record


def get_user_records(user_id):
    return (
        EmbedRecord.query.filter_by(user_id=user_id)
        .order_by(EmbedRecord.created_at.desc())
        .all()
    )


def get_record(record_id):
    return EmbedRecord.query.get(record_id)


def delete_embed_record(record):
    db.session.delete(record)
    db.session.commit()


def update_embed_record(record, payload):
    record.embed_payload = payload
    record.updated_at = datetime.utcnow()
    db.session.commit()
    return record
