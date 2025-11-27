import card
import deck
import game
import player

if __name__ == "__main__":
    my_game = game.Game
    alice = player.Player(game=my_game,name="alice")
    bob = player.Player(game=my_game,name="bob")
