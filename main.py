# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


from mancala import Board


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

game = Board()
game.print_board()

player = 0
while True:
    pocket = int(input("Player {0} please select a pocket (1-6)? ".format(player + 1)))
    if not(game.play(player, pocket-1)):
        if player == 0:
            player = 1
        else:
            player = 0

    game.print_board()


