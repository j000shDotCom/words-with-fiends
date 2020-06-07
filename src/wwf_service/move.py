from app.models import MoveModel

class Move:
    def __init__(self, move_dict):
        for k, v in move_dict.items():
            setattr(self, k, v)

    def is_play_move(self):
        return self.move_type == 'play'
    
    def get_model(self):
        return MoveModel(self)

    def __repr__(self):
        return str(self.__dict__)
