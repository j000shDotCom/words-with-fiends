from ..wwf_client import WwfClient

class WwfService():
    def login(self, login, password):
        wwf = WwfClient()
        r = wwf.login_with_email(login, password)
        print(r)
        return r

    def list_games(self, user):
        pass

    def make_game(self, type, user, challenger):
        pass

    def get_rewards(self, user):
        pass

    def make_move(self, game, user):
        pass

    def list_moves(self, game, user):
        pass
