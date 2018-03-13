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
FP_TILES_KNOWN = \
    '*' * 2 + \
    'E' * 7 + \
    'A' * 5 + \
    'I' * 4 + \
    'O' * 4 + \
    'N' * 2 + \
    'R' * 2 + \
    'T' * 2 + \
    'D' * 2 + \
    'L' * 2 + \
    'S' * 4 + \
    'U' * 1 + \
    'G' * 1 + \
    'B' * 1 + \
    'C' * 1 + \
    'F' * 1 + \
    'H' * 1 + \
    'M' * 1 + \
    'P' * 1 + \
    'V' * 1 + \
    'W' * 1 + \
    'Y' * 1 + \
    'J' * 1 + \
    'K' * 1 + \
    'Q' * 1 + \
    'X' * 1 + \
    'Z' * 1

# regular play
RP_BOARD_SIZE = 15
RP_TILE_COUNT = 104
RP_TILES = [None for _ in range(RP_TILE_COUNT)]
RP_MID = 6
RP_NUM_BLANKS = 2
RP_TILES_KNOWN = \
	'*' * 2 + \
	'E' * 13 + \
	'A' * 9 + \
	'I' * 8 + \
	'O' * 8 + \
	'N' * 5 + \
	'R' * 6 + \
	'T' * 7 + \
	'D' * 5 + \
	'L' * 4 + \
	'S' * 5 + \
	'U' * 4 + \
	'G' * 3 + \
	'B' * 2 + \
	'C' * 2 + \
	'F' * 2 + \
	'H' * 4 + \
	'M' * 2 + \
	'P' * 2 + \
	'V' * 2 + \
	'W' * 2 + \
	'Y' * 2 + \
	'J' * 1 + \
	'K' * 1 + \
	'Q' * 1 + \
	'X' * 1 + \
    'Z' * 1

# define context based on size
CONTEXT = {
    FP_BOARD_SIZE:
    {
        'TILE_COUNT': FP_TILE_COUNT,
        'TILES': FP_TILES,
        'TILES_KNOWN': FP_TILES_KNOWN,
        'MID': FP_MID,
        'BLANKS': FP_NUM_BLANKS
    },
    RP_BOARD_SIZE:
    {
        'TILE_COUNT': RP_TILE_COUNT,
        'TILES': RP_TILES,
        'TILES_KNOWN': RP_TILES_KNOWN,
        'MID': RP_MID,
        'BLANKS': RP_NUM_BLANKS
    }
}

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


def get_tiles_from_moves(moves):
    if not moves:
        return None

    if is_free_play(moves):
        TILES = FP_TILES
        BLANKS = FP_NUM_BLANKS
    else:
        TILES = RP_TILES
        BLANKS = RP_NUM_BLANKS

    tiles = {}
    for m in moves:
        if not is_play_move(m):
            continue

        word = m['words'][0].upper()
        x = m['from_x']
        y = m['from_y']

        # TODO figure out how to handle this case (YOWIE -> 0,o,45,15,4,)
        if len(word) != 1 + (m['to_y'] - y) + (m['to_x'] - x):
            print(f'Word bounds do not match', word, m['text'])
            continue

        # populate tiles
        move_tiles = {}
        i = 0
        for c in m['text'][:-1].split(','):
            if not c.isdigit():
                i += 1
            elif int(c) >= BLANKS:
                move_tiles[int(c)] = word[i]
                i += 1
            else:
                move_tiles[int(c)] = '*'

        tiles.update(move_tiles)

    populate_tiles(TILES, tiles)
    return tiles


def build_board_from_moves(moves):
    if not moves:
        return None

    if is_free_play(moves):
        SIZE = FP_BOARD_SIZE
    else:
        SIZE = RP_BOARD_SIZE

    board = [[' ' for _ in range(SIZE)] for _ in range(SIZE)]

    for m in moves:
        if not is_play_move(m):
            continue

        word = m['words'][0].upper()
        x = m['from_x']
        y = m['from_y']
        is_horizontal = m['from_y'] == m['to_y']

        # TODO figure out how to handle this case (YOWIE -> 0,o,45,15,4,)
        if len(word) != 1 + (m['to_y'] - y) + (m['to_x'] - x):
            print(f'Word bounds do not match', word, m['text'])
            continue

        # add characters to board
        for c in word:
            board[y][x] = c

            if is_horizontal:
                x += 1
            else:
                y += 1

    return board


def get_nums(moves):
    if not moves:
        return None

    if is_free_play(moves):
        SIZE = FP_BOARD_SIZE
        TILES = FP_TILES_KNOWN
    else:
        SIZE = RP_BOARD_SIZE
        TILES = RP_TILES_KNOWN

    board = [[None for _ in range(SIZE)] for _ in range(SIZE)]

    board_states = ""
    for m in moves:
        if not is_play_move(m):
            continue

        word = m['words'][0].upper()
        x = m['from_x']
        y = m['from_y']
        is_horizontal = m['from_y'] == m['to_y']

        # TODO figure out how to handle this case (YOWIE -> 0,o,45,15,4,)
        if len(word) != 1 + (m['to_y'] - y) + (m['to_x'] - x):
            print(f'Word bounds do not match', word, m['text'])
            continue

        for c in m['text'][:-1].split(','):
            if c.isdigit():
                board[y][x] = int(c)

                if is_horizontal:
                    x += 1
                else:
                    y += 1

        checksum = compute_checksum(board)
        diff = m['board_checksum'] - checksum
        board_states += f"{SIZE} {word} {m['text']}\n"
        board_states += f"{m['board_checksum']} {checksum} {diff}\n"
        board_states += f"{bin(m['board_checksum'])}\n"
        board_states += f"{bin(checksum)}\n"
        board_states += f"{board_to_str(board)}\n\n"

    return (board, board_states)


def compute_checksum(board):
    SIZE = len(board)
    checksum = 0 if SIZE > 12 else (2 ** 25 - 1)
    b = 0
    for (y, row) in enumerate(board):
        for (x, tile) in enumerate(row):
            if tile == None:
                checksum ^= 1
            elif tile == 0 or tile == 1:
                checksum ^= 2 ** ((15 * y + x) % 32)
                b += 1
            else:
                checksum ^= tile
                b += 1

    if b % 2 == 1:
        checksum = -checksum

        if (checksum ^ 2) % 2 == 0:
            checksum -= 2

    return checksum


def is_play_move(m):
    return m['move_type'] == 'play' and m['text'] and m['words']


def populate_tiles(tile_list, tiles):
    for (i, c) in tiles.items():
        tile_list[i] = c


def is_free_play(moves):
    m = moves[0] if type(moves) == list else moves
    horizontal = m['from_y'] == FP_MID and m['to_y'] == FP_MID
    vertical = m['from_x'] == FP_MID and m['to_x'] == FP_MID
    return horizontal or vertical


def board_to_str(board):
    LETS = RP_TILES_KNOWN if len(board) > 12 else FP_TILES_KNOWN
    b = '  ' + ' '.join(map(str, [i % 10 for i in range(len(board))]))
    i = 0
    for row in board:
        row = map(lambda x: ' ' if x is None else LETS[x], row)
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
