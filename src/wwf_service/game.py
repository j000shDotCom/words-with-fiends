from app.models import GameModel

FP_BOARD_SIZE = 11
FP_TILES = '**EEEEEEEAAAAAIIIIOOOONNRRTTDDLLSSSSUGBCFHMPVWYJKQXZ'

RP_BOARD_SIZE = 15
RP_TILES = '**EEEEEEEEEEEEEAAAAAAAAAIIIIIIIIOOOOOOOONNNNNRRRRRR' \
         + 'TTTTTTTDDDDDLLLLSSSSSUUUUGGGBBCCFFHHHHMMPPVVWWYYJKQXZ'

CONTEXT = {
    FP_BOARD_SIZE: {'tiles': FP_TILES, 'mid': 5},
    RP_BOARD_SIZE: {'tiles': RP_TILES, 'mid': 6}
}

class Game:
    def __init__(self, game_dict):
        for k,v in game_dict.items():
            setattr(self, k, v)

        self.moves = [Move(m) for m in self.moves]
        self.board = build_board_from_moves(self.moves)
        self.tiles = get_remaining_tiles(self.board)

    def can_make_move(self, user):
        return self.days_left > 0 and self.current_move_user_id == user.id

    def get_next_legal_move(self):
        pass

    def get_next_illegal_move(self):
        tiles = get_random_subset(self.tiles)
        print(tiles)
        pass

    def get_model(self):
        rem = ['moves', 'users']
        game_dict = {k:self.__dict__[k] for k in self.__dict__ if k not in rem}
        return GameModel(**game_dict)

    def compute_checksum(self, board):
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

    def __repr__(self):
        return str(self.__dict__)

### HELPER METHODS ###

def is_free_play(moves):
    m = moves[0] if type(moves) == list else moves
    mid = CONTEXT[FP_BOARD_SIZE]['mid']
    horizontal = m.from_y == mid and m.to_y == mid
    vertical = m.from_x == mid and m.to_x == mid
    return horizontal or vertical

def get_random_subset(tile_map, num = 7):
    remaining = list(itertools.chain.from_iterable(tiles.values()))
    return random.sample(remaining, num)

def get_remaining_tiles(board):
    tiles = CONTEXT[len(board)]['tiles']

    # pop off tiles used on the board
    num_set = set(range(len(tiles)))
    for row in board:
        for t in row:
            if t:
                num_set.remove(t)

    # build letter to ordinal map
    tile_map = {}
    for c in num_set:
        letter = tiles[c]
        if letter not in tile_map:
            tile_map[letter] = [c]
        else:
            tile_map[letter].append(c)

    return tile_map

def build_board_from_moves(moves):
    size = FP_BOARD_SIZE if is_free_play(moves) else RP_BOARD_SIZE
    board = [[None for _ in range(size)] for _ in range(size)]

    for m in moves:
        if not m.is_play_move():
            continue

        word = m.words[0].upper()
        x = m.from_x
        y = m.from_y
        is_horizontal = m.from_y == m.to_y

        # TODO figure out how to handle this case (YOWIE -> 0,o,45,15,4,)
        if len(word) != 1 + (m.to_y - y) + (m.to_x - x):
            print(f'Word bounds do not match', word, m.text)
            continue

        chars = m.text[:-1].split(',') # remove trailing comma
        for c in chars:
            if c.isdigit():
                board[y][x] = int(c)
                if is_horizontal:
                    x += 1
                else:
                    y += 1

    return board
