from models.user_devices import user_devices
from repository.AbstractRepository import AbstractRepository


class user_devicesRepository(AbstractRepository):
    def __init__(self):
        self.entity = user_devices
