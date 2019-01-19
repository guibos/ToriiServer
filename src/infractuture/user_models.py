"""User models."""

from sqlalchemy import Column, Integer, DateTime, String, Date, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base

from src.domain.entities.user_entity import UserEntity

BASE = declarative_base()
SCHEMA = 'account'


class UserModel(BASE):
    """User model."""
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False, index=True)
    password = Column(JSON, nullable=False)
    sign_up = Column(DateTime(timezone=True), nullable=False)
    enabled = Column(Boolean, nullable=False)
    session_active = Column(DateTime(timezone=True), nullable=False)
    admin = Column(Boolean, nullable=False)
    parental_control = Column(Boolean, nullable=False)
    birth_date = Column(Date)
    # attr_to_field = {
    #     UserEntity.id: id,
    #     UserEntity.username: username,
    #     UserEntity.password: password,
    #     UserEntity.sign_up: sign_up,
    #     UserEntity.enabled: enabled,
    #     UserEntity.session_active: session_active,
    #     UserEntity.admin: admin,
    #     UserEntity.parental_control: parental_control,
    #     UserEntity.birth_date: birth_date,
    # }
    entity = UserEntity

    @classmethod
    def from_domain_data(cls, *, user_entity: UserEntity):
        data = user_entity.__dict__
        data['password'] = data['password'].__dict__
        return cls(**data)
