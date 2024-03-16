from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey, func

from config.db import Base


class user_nakama(Base):
    __tablename__ = 'user_nakama'

    id_nakama = Column('id_nakama',Integer, primary_key=True, autoincrement=True)
    id_user_follower = Column(Integer, ForeignKey('user_data.id_user'), nullable=False)
    id_user_leader = Column(Integer, ForeignKey('user_data.id_user'), nullable=False)
    follow_creation = Column(DateTime, default=func.now())
    nakama_creation = Column(DateTime)
    is_blocked = Column(Boolean, default=False)
    you_are_blocked = Column(Boolean, default=False)
    is_followed_back = Column(Boolean, default=False)

    def __repr__(self):
        return (f"UserNakama(id_nakama={self.id_nakama}, "
                f"id_user_follower={self.id_user_follower}, "
                f"id_user_leader={self.id_user_leader}, "
                f"follow_creation={self.follow_creation}, "
                f"nakama_creation={self.nakama_creation}, "
                f"is_blocked={self.is_blocked}, "
                f"you_are_blocked={self.you_are_blocked}, "
                f"is_followed_back={self.is_followed_back})")

