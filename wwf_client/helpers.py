# fast play
FP_BOARD_SIZE = 11
FP_TILES = \
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
RP_TILES = \
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

# define context based on board size
CONTEXT = {
    FP_BOARD_SIZE: {'tiles': FP_TILES, 'mid': 5},
    RP_BOARD_SIZE: {'tiles': RP_TILES, 'mid': 6 }
}

def get_blank_board(moves, unused_tile_char = None):
    if not moves:
        return None

    if is_free_play(moves):
        SIZE = FP_BOARD_SIZE
    else:
        SIZE = RP_BOARD_SIZE

    return [[unused_tile_char for _ in range(SIZE)] for _ in range(SIZE)]

def build_text_board_from_moves(moves):
    board = get_blank_board(moves, ' ')

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

def build_num_board_from_moves(moves):
    board = get_blank_board(moves)

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

        # board_to_str(board)

        # checksum = compute_checksum(board)
        # diff = m['board_checksum'] - checksum
        # board_states += f"{SIZE} {word} {m['text']}\n"
        # board_states += f"{m['board_checksum']} {checksum} {diff}\n"
        # board_states += f"{bin(m['board_checksum'])}\n"
        # board_states += f"{bin(checksum)}\n"
        # board_states += f"{board_to_str(board)}\n\n"

    return board

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

def board_to_str(board, **kwargs):
    tiles = CONTEXT[len(board)]['tiles']
    vertical_delim = '|' if 'vert' in kwargs else ''
    b = '  ' + vertical_delim.join(map(str, [i % 10 for i in range(len(board))]))
    i = 0
    for row in board:
        row = [x if x else ' ' for x in row]
        line = '\n' + str(i % 10) + ' '
        line += vertical_delim.join(row)
        b += line
        
        if 'horiz' in kwargs:
            b += '\n' + ''.join(['-' for _ in range(len(line))])
        i += 1
    return b

def is_play_move(m):
    return m['move_type'] == 'play' and m['text'] and m['words']

def is_free_play(moves):
    # get first move
    m = moves[0] if type(moves) == list else moves
    mid = CONTEXT[FP_BOARD_SIZE]['mid']
    horizontal = m['from_y'] == mid and m['to_y'] == mid
    vertical = m['from_x'] == mid and m['to_x'] == mid
    return horizontal or vertical

def game_is_valid(game):
    return game['days_left'] > 0
