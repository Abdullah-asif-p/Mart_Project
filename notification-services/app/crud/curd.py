from typing import List, Optional
from sqlmodel import Session, select

from app.models.notification import Notifications


def get_notifications(db: Session, user_id:str ):
    """Retrieve a list of notifications."""
    statement = select(Notifications).where(Notifications.user_id == user_id)
    results = db.exec(statement).all()  # Correctly fetch all matching notifications
    return results


# def get_notification(db: Session, notification_id: int) -> Optional[Notifications]:
#     """Retrieve a specific notification by ID."""
#     statement = select(Notifications).where(Notifications.id == notification_id)
#     return db.exec(statement).first()


def create_notification(db: Session, notifications: Notifications):
    """Create a new notification."""
    db.add(notifications)
    db.commit()
    db.refresh(notifications)
    return notifications


def update_notification(db: Session, notification_id: int, status: str) -> Optional[Notifications]:
    """Update the status of a notification."""
    notification = db.exec(select(Notifications).where(Notifications.id == notification_id)).first()
    if notification:
        notification.status = status
        db.add(notification)
        db.commit()
        db.refresh(notification)
        return notification
    return None


def delete_notification(db: Session, notification_id: int) -> None:
    """Delete a notification."""
    notification = db.exec(select(Notifications).where(Notifications.id == notification_id)).first()
    if notification:
        db.delete(notification)
        db.commit()
