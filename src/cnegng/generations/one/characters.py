from cnegng.ACME import BasicStats


def basic_player():
    """
    Creates a basic player with 60 maximum life.

    :return: A Player object with 'maximum_life' set to 60.
    """
    return BasicStats(
        intelligence=20,
        dexterity=20,
        strength=20,
        level=1,
        life=60,
        maximum_life=60,
        mana=50,
        maximum_mana=50,
        fire_resistance=0,
        cold_resistance=0,
        lightning_resistance=0,
        chaos_resistance=0,
    )
