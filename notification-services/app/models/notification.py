from datetime import datetime
from typing import Optional, List
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship

# Define the NotificationStatus enum
# class NotificationStatus(str, Enum):
#     PENDING = "PENDING"
#     SENT = "SENT"
#     FAILED = "FAILED"

# Define the NotificationType enum
# class NotificationType(str, Enum):
#     EMAIL = "EMAIL"
#     SMS = "SMS"
#     PUSH = "PUSH"

# User model
# class User(SQLModel, table=True):
#     __tablename__ = 'users'

#     user_id: Optional[str] = Field(default=None, primary_key=True)
#     email: str = Field()
#     notifications: List["Notification"] = Relationship(back_populates="user")


# Notification model
# class Notification(SQLModel, table=True):
#     __tablename__ = 'notifications'

#     id: Optional[int] = Field(default=None, primary_key=True)
#     message: str
#     user_id: str
#     timestamp: str
# notification_type: NotificationType = Field(nullable=False)

# user: Optional[User] = Relationship(back_populates="notifications")



class Notifications(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    message: str
    user_id: str
    time: str
