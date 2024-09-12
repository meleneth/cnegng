from cnegng.ACME import ItemWithModifiers, AttributeModifier, LootTable


def ring_of_power():
    """

    Creates a ring that adds a flat +10 to 'strength'.


    :return: An ItemWithModifiers object with a +10 'flat' modifier to 'strength'.

    """
    return ItemWithModifiers(AttributeModifier.create_flat("strength", 10))


def ring_of_agility():
    """

    Creates a ring that adds a flat +5 to 'agility'.


    :return: An ItemWithModifiers object with a +5 'flat' modifier to 'agility'.

    """
    return ItemWithModifiers(AttributeModifier.create_flat("agility", 5))


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
