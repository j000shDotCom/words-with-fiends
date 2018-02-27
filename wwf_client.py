"""
 Simple bot to log into and play WWF
"""
from requests import Session
import json


# main constants
HOST = 'https://wordswithfriends.zyngawithfriends.com'
BUNDLE_NAME = 'WordsWithFriends3'
CLIENT_VERSION = '10.26'

# fast play
FP_BOARD_SIZE = 11
FP_TILE_COUNT = 52
FP_TILES = [None for _ in range(FP_TILE_COUNT)]
FP_MID = 5
FP_NUM_BLANKS = 2

# regular play
RP_BOARD_SIZE = 15
RP_TILE_COUNT = 104
RP_TILES = [None for _ in range(RP_TILE_COUNT)]
RP_MID = 6
RP_NUM_BLANKS = 2

# tiles
VALID_CHARACTERS = [chr(c) for c in range(ord('A'), ord('Z') + 1)]
WWF_TILE_IDS = {c: set() for c in VALID_CHARACTERS}

# defined in config request
MAX_ACTIVE = 0
BLACKLIST = []
WHITELIST = []


def _log_request_status(r, *args, **kwargs):
    parts = [r.status_code, r.request.method, r.request.url]
    if r.request.body:
        parts.append(r.request.body)
    print(*parts)

    if not r.ok:
        parts.append(r.text)
        raise ValueError('Request Failed: ', *parts)


def get_initial_config():
    s = Session()

    s.hooks['response'].append(_log_request_status)
    s.headers.update({'Accept': 'application/json'})

    url = '/jumps/config'
    query = {
        'bundle_name': BUNDLE_NAME,
        'client_version': CLIENT_VERSION,
        'plaintext': 1,
    }

    # initial config
    r = s.get(HOST + url, params=query)
    d = json.loads(r.text)
    MAXACTIVE = int(d['MaxActiveGamesForCreate'])
    BLACKLIST.extend(d['BlackListedWords'].split(','))
    WHITELIST.extend(d['WhiteListedWords'].split(','))
    return s


def login(login, password):
    s = get_initial_config()
    url = '/sessions/create'
    data = {
        'login_request': {'login': login, 'password': password}
    }
    s.post(HOST + url, json=data)
    return s


def get_user_data(s):
    url = '/user_data'
    params = {
        'badges': True,
        'game_type': 'WordGame',
        'include_item_data': True
    }
    r = s.get(HOST + url, params=params)
    d = json.loads(r.text)
    return r


def get_games(s):
    url = '/games'
    params = {
        'game_type': 'WordGame',
        'get_current_user': True,
        'include_invitations': True,
        'include_item_data': True,
        'chat_messages_since': 0,
        'moves_since': 0
    }
    r = s.get(HOST + url, params=params)
    d = json.loads(r.text)
    return d['games']


def build_board(g):
    moves = g['moves']
    if not moves:
        return None

    if is_free_play(moves):
        SIZE = FP_BOARD_SIZE
        TILES = FP_TILES
        BLANKS = FP_NUM_BLANKS
    else:
        SIZE = RP_BOARD_SIZE
        TILES = RP_TILES
        BLANKS = RP_NUM_BLANKS

    board = [[' ' for _ in range(SIZE)] for _ in range(SIZE)]

    for m in moves:
        print_move(m)
        if not is_move_play(m):
            continue

        tiles = {}
        word = m['words'][0].upper()
        x = m['from_x']
        y = m['from_y']
        is_horizontal = m['from_y'] == m['to_y']

        # add characters to board
        for c in word:
            board[y][x] = c

            if is_horizontal:
                x += 1
            else:
                y += 1

        # build tiles
        i = 0
        for c in m['text'][:-1].split(','):
            if not c.isdigit():
                i += 1
                continue
            if int(c) >= BLANKS:
                tiles[int(c)] = word[i]
                i += 1
            else:
                tiles[int(c)] = '*'

        # populate global tile map
        for (i, c) in tiles.items():
            TILES[i] = c

    return board


def is_move_play(m):
    return m['move_type'] == 'play' and m['text'] and m['words']


def print_move(m):
    pos = "{} -> {}".format((m['from_x'], m['from_y']), (m['to_x'], m['to_y']))
    print(m['move_index'], m['move_type'], m['text'], m['words'], pos)


def is_free_play(moves):
    m = moves[0] if type(moves) == list else moves
    horizontal = m['from_y'] == FP_MID and m['to_y'] == FP_MID
    vertical = m['from_x'] == FP_MID and m['to_x'] == FP_MID
    return horizontal or vertical


def board_to_str(board):
    b = '  ' + ' '.join(map(str, [i % 10 for i in range(len(board))]))
    b += '\n'
    i = 0
    for row in board:
        b += '\n' + str(i % 10) + ' ' + '|'.join(row)
        i += 1
    return b


def game_is_valid(game):
    return game['days_left'] > 0


def get_next_move(letters, state):
    pass


def make_move(s, move):
    pass


def get_chat_messages(s, user):
    pass


def get_daily_drip(s):
    url = '/packages/grant_daily_drip'
    return s.get(HOST + url)
