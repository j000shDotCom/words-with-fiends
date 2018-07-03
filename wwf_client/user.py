from app.models import UserModel

class User:
    def __init__(self, user_dict):
        for k, v in user_dict.items():
            setattr(self, k, v)

    def get_model(self):
        return UserMode(self)

    def __repr__(self):
        return str(self.__dict__)
