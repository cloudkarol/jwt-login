from abc import abstractclassmethod

class BaseService():
    @abstractclassmethod
    def save():
        ...
    @abstractclassmethod
    def get_by_id():
        ...