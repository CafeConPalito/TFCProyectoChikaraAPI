from sqlalchemy import Column, Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from config.db import Base


class user_log(Base):
    __tablename__ = 'user_log'

    id = Column('id_log',Integer, primary_key=True, autoincrement=True)
    id_user = Column(Integer, ForeignKey('user_data.id_user'), nullable=False)
    log_in = Column(DateTime(timezone=True), default=func.now())
    log_out = Column(DateTime(timezone=True))

    def __repr__(self):
        return f"<UserLog(id_log={self.id_log}, id_user={self.id_user}, log_in={self.log_in}, log_out={self.log_out})>"