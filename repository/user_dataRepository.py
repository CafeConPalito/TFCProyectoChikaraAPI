
from models.user_data import user_data
from repository.AbstractRepository import AbstractRepository


class User_DataRepository(AbstractRepository):
    def __init__(self):
        self.entity = user_data