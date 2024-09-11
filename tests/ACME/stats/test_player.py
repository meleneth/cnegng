from cnegng.generations.one.characters import basic_player


def test_basic_player_is_basic():
    player = basic_player()
    assert player.maximum_life == 60
