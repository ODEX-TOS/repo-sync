import json
import os
import errno
import time
from .config import *



class Persist():
    def __init__(self):
        self.modification_time = 0
        self.type = DEPLOY_TYPE
        self.backend = DEPLOY_BACKEND
        self.domain = DEPLOY_DOMAIN
        self.ring = RING_LEVEL
        self.path = DEPLOY_PATH

    def update_time(self) -> None:
        self.modification_time = time.time()

    def to_dict(self) -> dict:
        return {
            "ring": self.ring,
            "modification_time": self.modification_time,
            "type": self.type,
            "backend": self.backend,
            "domain": self.domain,
            "path": self.path
        }

    def from_dict(self, _dict: dict) -> None:
        self.modification_time = _dict["modification_time"]
        self.type = _dict["type"]
        self.backend = _dict["backend"]
        self.domain = _dict["domain"]
        self.ring = _dict["ring"]
        self.path = _dict["path"]


def create_data_dir(_dir=DATA_STORAGE):
    dir = os.path.dirname(_dir)
    if not os.path.exists(dir):
        try:
            os.makedirs(dir)
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    

def save(data: Persist) -> None:
    _dict = data.to_dict()

    create_data_dir()

    with open(DATA_STORAGE, 'w') as outfile:
        json.dump(_dict, outfile)

def load() -> Persist:
    persist = Persist()

    try:
        with open(DATA_STORAGE, 'r') as jsonFile:
            jsonObject = json.load(jsonFile)
            persist.from_dict(jsonObject)
    except:
        pass

    return persist