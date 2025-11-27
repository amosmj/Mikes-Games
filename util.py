import gc

import player

def get_all_players():
    player_list = []
    all_objects = gc.get_objects()
    for obj in all_objects:
        if isinstance(obj, player.Player):
            player_list.append(player)
    return player_list