from cnegng.ACME import BasicStats, ItemWithModifiers, AttributeModifier


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


def small_vit_ring():
    """

    Creates a ring that adds a flat +20 to 'maximum_life'.


    :return: An ItemWithModifiers object with a +20 'flat' modifier to 'maximum_life'.

    """
    return ItemWithModifiers(AttributeModifier("maximum_life", "flat", 20))


def percent_life_ring():
    """
    Creates a ring that increases 'maximum_life' by 50% (1.5x multiplier).


    :return: An ItemWithModifiers object with a 50% 'percent' modifier to 'maximum_life'.
    """
    return ItemWithModifiers(AttributeModifier("maximum_life", "percent", 0.5))
