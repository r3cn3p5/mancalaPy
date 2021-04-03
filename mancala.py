class BoardSide(object):

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


class Board(object):

    def __init__(self):

        self._sides = []
        for s in range(0, 2):
            self._sides.append(BoardSide())

    def validate_move(self, player, pocket):

        if 0 < player > 1:
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
                    if stones == 1:
                        replay = True
                    else:
                        replay = False
                    stones -= 1

                pocket = 0

                # switch sides and continue
                if side == 0:
                    side = 1
                else:
                    side = 0

                continue

            # if last stone on player pocket take other side.
            if side == player and stones == 1 and self._sides[side].pockets[pocket] == 0:
                self._sides[side].store += 1
                self._sides[side].pockets[pocket] = 0

                if side == 0:
                    self._sides[side].store = self._sides[1].pockets[pocket]
                    self._sides[1].pockets[pocket] = 0
                else:
                    self._sides[side].store = self._sides[0].pockets[pocket]
                    self._sides[0].pockets[pocket] = 0

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

    def __str__(self):

        str = "S({0:2d}) ".format(self._sides[0].store)

        for p in range(5, -1, -1):
            str += "{0:1d}({1:2d}) ".format(p + 1, self._sides[0].pockets[p])
        str += "\n"

        str += "      "
        for p in range(0, 6):
            str += "{0:1d}({1:2d}) ".format(p + 1, self._sides[1].pockets[p])
        str += "S({0:2d})".format(self._sides[1].store)

        return str
