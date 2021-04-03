class BoardSide(object):

    def __init__(self):
        self.store = 0

        self.pockets = []
        for x in range(0, 6):
            self.pockets.append(4)


class Board(object):

    def __init__(self):

        self.sides = []
        for s in range(0, 2):
            self.sides.append(BoardSide())

    def play(self, player, pocket):

        replay = False

        # player can only by 0 or 1
        side = player

        # lets get the initial
        stones = self.sides[side].pockets[pocket]
        self.sides[side].pockets[pocket] = 0
        pocket += 1

        while stones > 0:

            if pocket >= 6:

                # drop into store if players side
                if side == player:
                    self.sides[side].store += 1

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
            if side == player and stones == 1 and self.sides[side].pockets[pocket] == 0:
                self.sides[side].store += 1
                self.sides[side].pockets[pocket] = 0

                if side == 0:
                    self.sides[side].store = self.sides[1].pockets[pocket]
                    self.sides[1].pockets[pocket] = 0
                else:
                    self.sides[side].store = self.sides[0].pockets[pocket]
                    self.sides[0].pockets[pocket] = 0

                break

            # standard old go.
            self.sides[side].pockets[pocket] += 1
            stones -= 1
            pocket += 1

        # if one player has empty side then the other takes all there remaining stones.
        for s in range(0, 2):

            t = 0
            for p in range(0, 6):
                t += self.sides[s].pockets[p]

            if t == 0:
                for p in range(0, 6):
                    if s == 0:
                        t += self.sides[1].pockets[p]
                        self.sides[1].pockets[p] = 0
                    else:
                        t += self.sides[0].pockets[p]
                        self.sides[0].pockets[p] = 0

                if s == 0:
                    self.sides[1].store += t
                else:
                    self.sides[0].store += t

                break

        return replay

    def print_board(self):

        print("S({0:2d}) ".format(self.sides[0].store), end='')
        for p in range(5, -1, -1):
            print("({0:2d}) ".format(self.sides[0].pockets[p]), end='')
        print()

        print("      ", end='')
        for p in range(0, 6):
            print("({0:2d}) ".format(self.sides[1].pockets[p]), end='')
        print("S({0:2d})".format(self.sides[1].store), end='')
        print()
