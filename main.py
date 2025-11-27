import card
import deck
import game
import player



if __name__ == "__main__":
    my_game = game.Game
    player1 = player.Player(game=my_game,name="alice")
    player2 = player.Player(game=my_game,name="bob")



    del player1
    del player2
    del my_game
