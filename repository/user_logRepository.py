from models.user_log import user_log
from repository.AbstractRepository import AbstractRepository


class User_LogRepository(AbstractRepository):
    def __init__(self):
        self.entity = user_log