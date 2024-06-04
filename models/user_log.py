from sqlalchemy import Column, Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

from config.db import Base


class user_log(Base):
    __tablename__ = 'user_log'

    id = Column('id_log',UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_user = Column(UUID(as_uuid=True), ForeignKey('user_data.id_user'), nullable=False)
    log_in = Column(DateTime(timezone=True), default=func.now())
    log_out = Column(DateTime(timezone=True))

    def __repr__(self):
        return f"<UserLog(id_log={self.id_log}, id_user={self.id_user}, log_in={self.log_in}, log_out={self.log_out})>"