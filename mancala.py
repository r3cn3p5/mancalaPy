class BoardSide:

    def __init__(self):
        self._store = 0
        self._pockets = []
        for x in range(0, 6):
            self.pockets.append(4)

    @property
    def store(self):
        return self._store

    @store.setter
    def store(self, store):
        self._store = store

    @property
    def pockets(self):
        return self._pockets


class Board:
    STATUS_IN_PROGRESS = 0
    STATUS_PLAYER_ONE_WINS = 1
    STATUS_PLAYER_TWO_WINS = 2
    STATUS_DRAW = 3
    STATUS_PLAYER_REPLAY = 4
    STATUS_INVALID_MOVE_NO_STONES = 5

    def __init__(self):

        self._sides = []
        for s in range(0, 2):
            self._sides.append(BoardSide())

    def make_move(self, player, pocket):
        """

        :param player:
        :param pocket:
        :return:
        """

        if self._sides[player].pockets[pocket] == 0:
            return Board.STATUS_INVALID_MOVE_NO_STONES

        status = Board.STATUS_IN_PROGRESS
        side = player

        # lets get the initial
        stones = self._sides[side].pockets[pocket]
        self._sides[side].pockets[pocket] = 0
        pocket += 1

        while stones > 0:

            if pocket >= 6:

                # drop into store if players side
                if side == player:
                    self._sides[side].store += 1

                    # last stone the player gets another go
                    status = Board.STATUS_PLAYER_REPLAY if stones == 1 else status
                    stones -= 1

                pocket = 0

                # switch sides and continue
                side = 1 if side == 0 else 0

                continue

            # if last stone on player pocket take other side.
            opposite_side = 1 if side == 0 else 0
            if side == player \
                    and stones == 1 \
                    and self._sides[side].pockets[pocket] == 0 \
                    and self._sides[opposite_side].pockets[5 - pocket] > 0:
                self._sides[side].store += 1
                self._sides[side].pockets[pocket] = 0
                self._sides[side].store += self._sides[opposite_side].pockets[5 - pocket]
                self._sides[opposite_side].pockets[5 - pocket] = 0
                break

            # standard old go.
            self._sides[side].pockets[pocket] += 1
            stones -= 1
            pocket += 1

        # if one player has empty side then the other takes all there remaining stones.
        for s in range(0, 2):
            os = 1 if s == 0 else 0

            t = 0
            for p in range(0, 6):
                t += self._sides[s].pockets[p]

            if t == 0:
                for p in range(0, 6):
                    t += self._sides[os].pockets[p]
                    self._sides[os].pockets[p] = 0

                self._sides[os].store += t

                if self._sides[0].store > self._sides[1].store:
                    status = Board.STATUS_PLAYER_ONE_WINS
                elif self._sides[0].store < self._sides[1].store:
                    status = Board.STATUS_PLAYER_TWO_WINS
                else:
                    status = Board.STATUS_DRAW

                break

        return status

    def __str__(self):

        ret_str = "S({0:2d}) ".format(self._sides[0].store)

        for p in range(5, -1, -1):
            ret_str += "{0:1d}({1:2d}) ".format(p + 1, self._sides[0].pockets[p])
        ret_str += "\n"

        ret_str += "      "
        for p in range(0, 6):
            ret_str += "{0:1d}({1:2d}) ".format(p + 1, self._sides[1].pockets[p])
        ret_str += "S({0:2d})".format(self._sides[1].store)

        return ret_str


def get_pocket_from_player(player):
    while True:
        pocket_input = input("Player {0} please select a pocket (1-6)? ".format(player + 1))

        if pocket_input.isnumeric():
            pocket_int = int(pocket_input)-1

            if -1 <= pocket_int < 6:
                return pocket_int


if __name__ == '__main__':
    print('Lets play Mancala')

    game = Board()
    print(game)

    current_player = 0
    while True:
        selected_pocket = get_pocket_from_player(current_player)

        if selected_pocket == -1:
            break

        game_status = game.make_move(current_player, selected_pocket)

        print(game)

        if game_status == Board.STATUS_IN_PROGRESS:
            current_player = 1 if current_player == 0 else 0
        elif game_status == Board.STATUS_PLAYER_ONE_WINS:
            print ("Player 1 has won!")
            break
        elif game_status == Board.STATUS_PLAYER_TWO_WINS:
            print ("Player 2 has won!")
            break
        elif game_status == Board.STATUS_DRAW:
            print("Draw!")
            break
        elif game_status == Board.STATUS_PLAYER_REPLAY:
            print("You get another go!")
        elif game_status == Board.STATUS_INVALID_MOVE_NO_STONES:
            print("Ooops no stones in that pocket")
            pass

    print("Game Over")