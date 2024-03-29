from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, func
from sqlalchemy.dialects.postgresql import UUID
import uuid

from config.db import Base

class user_data(Base):
    __tablename__ = 'user_data'

    id = Column('id_user',UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_name = Column(String(150), nullable=False)
    email = Column(String(300), nullable=False)
    pwd = Column(String(300), nullable=False)
    first_name = Column(String(150), nullable=False)
    first_last_name = Column(String(150), nullable=False)
    second_last_name = Column(String(150))
    birthdate = Column(Date, nullable=False)
    account_creation = Column(DateTime(timezone=True), default=func.now())
    is_premium = Column(Boolean, default=False)

    def __repr__(self):
        return (f"<UserData(id_user={self.id_user}, user_name='{self.user_name}', "
                f"email='{self.email}', password='{self.password}', "
                f"first_name='{self.first_name}', first_last_name='{self.first_last_name}', "
                f"second_last_name='{self.second_last_name}', birthdate='{self.birthdate}', "
                f"account_creation='{self.account_creation}', is_premium={self.is_premium})>")
