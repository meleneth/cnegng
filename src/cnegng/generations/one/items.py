from cnegng.ACME import ItemWithModifiers, AttributeModifier, LootTable


def small_vit_ring():
    """

    Creates a ring that adds a flat +20 to 'maximum_life'.


    :return: An ItemWithModifiers object with a +20 'flat' modifier to 'maximum_life'.

    """
    return ItemWithModifiers(AttributeModifier.create_flat("maximum_life", 20))


def percent_life_ring():
    """
    Creates a ring that increases 'maximum_life' by 50% (1.5x multiplier).


    :return: An ItemWithModifiers object with a 50% 'percent' modifier to 'maximum_life'.
    """
    return ItemWithModifiers(AttributeModifier.create_percent("maximum_life", 0.5))


def boss_helm():
    """
    Creates a helm that is so boss.


    :return: An ItemWithModifiers object with a 50% 'percent' modifier to 'maximum_life'.
    """
    return ItemWithModifiers(AttributeModifier.create_percent("maximum_life", 0.5))
