from mancala import Board


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
            print("Player 1 has won!")
            break
        elif game_status == Board.STATUS_PLAYER_TWO_WINS:
            print("Player 2 has won!")
            break
        elif game_status == Board.STATUS_DRAW:
            print("Draw!")
            break
        elif game_status == Board.STATUS_PLAYER_REPLAY:
            print("You get another go!")
        elif game_status == Board.STATUS_INVALID_MOVE_NO_STONES:
            print("Oh dear no stones in that pocket")

    print("Game Over")
