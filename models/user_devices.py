from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, func, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

from config.db import Base


class user_devices(Base):
    __tablename__ = 'user_device'

    id = Column('id_device',UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_user = Column(UUID(as_uuid=True), ForeignKey('user_data.id_user'), nullable=False)
    phone_id = Column(String(150), nullable=False, unique=True)
    phone_model = Column(String(150), nullable=False)
    phone_brand = Column(String(150), nullable=False)
    block = Column(Boolean, nullable=False, default=False)
