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

    def __init__(self):

        self._sides = []
        for s in range(0, 2):
            self._sides.append(BoardSide())

    def validate_move(self, player, pocket):

        if not 0 <= player <= 1:
            print("Invalid player {}".format(player + 1))
            return False

        if not 0 <= pocket <= 5:
            print("Invalid pocket {}".format(pocket + 1))
            return False

        if self._sides[player].pockets[pocket] == 0:
            print("Not stones left")
            return False

        return True

    def make_move(self, player, pocket):

        replay = False

        # player can only by 0 or 1
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
                    replay = True if stones == 1 else False

                    stones -= 1

                pocket = 0

                # switch sides and continue
                side = 1 if side == 0 else 0

                continue

            # if last stone on player pocket take other side.
            opposite_side = 1 if side == 0 else 0
            if side == player and stones == 1 and self._sides[side].pockets[pocket] == 0 and self._sides[opposite_side].pockets[5 - pocket] > 0:
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

            t = 0
            for p in range(0, 6):
                t += self._sides[s].pockets[p]

            if t == 0:
                for p in range(0, 6):
                    if s == 0:
                        t += self._sides[1].pockets[p]
                        self._sides[1].pockets[p] = 0
                    else:
                        t += self._sides[0].pockets[p]
                        self._sides[0].pockets[p] = 0

                if s == 0:
                    self._sides[1].store += t
                else:
                    self._sides[0].store += t

                break

        return replay

    def has_a_player_won(self):

        s1 = s2 = 0
        for p in range(0, 6):
            s1 += self._sides[0].pockets[p]
            s2 += self._sides[1].pockets[p]

        if s1 == 0 or s2 == 0:
            if self._sides[0].store > self._sides[1].store:
                return 0
            elif self._sides[0].store < self._sides[1].store:
                return 1
            else:
                return 3

        return -1

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


if __name__ == '__main__':
    print('Lets play Mancala')

    game = Board()
    print(game)

    current_player = 0
    while True:
        selected_pocket = int(input("Player {0} please select a pocket (1-6)? ".format(current_player + 1))) - 1

        if selected_pocket == -1:
            break

        if not game.validate_move(current_player, selected_pocket):
            continue

        replay_again = game.make_move(current_player, selected_pocket)

        game_state = game.has_a_player_won()
        if game_state >= 0:
            print(game)
            if game_state == 3:
                print("Draw!")
            else:
                print("Player {} has won!".format(game_state + 1))
            break

        if not replay_again:
            current_player = 1 if current_player == 0 else 0

        print(game)

    print("Game Over")
