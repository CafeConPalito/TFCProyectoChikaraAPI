
from models.user_nakama import user_nakama
from repository.AbstractRepository import AbstractRepository


class User_NakamaRepository(AbstractRepository):
    def __init__(self):
        self.entity = user_nakama