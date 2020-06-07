
def store_games(games):
    for g in games:
        users = g['users']
        moves = g['moves'] if 'moves' in g else []

        store_thing(UserModel, g['users'])
        store_thing(GameModel, [{k:g[k] for k in g if k not in ['moves', 'users']}])

        for m in moves:
            m['word'] = m['words'][0] if m['words'] else ''
        store_thing(MoveModel, moves)

def store_thing(self, CL, objs):
    try:
        for ob in objs:
            e = CL(**ob)
            db.session.merge(e)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
