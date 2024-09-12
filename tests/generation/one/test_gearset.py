import pytest
from cnegng.ACME.stats.item_with_modifiers import ItemWithModifiers
from cnegng.generations.one.gear_set import GearSet
from cnegng.generations.one.items import ring_of_power, ring_of_agility
from cnegng.generations.one.characters import basic_player


def test_gear_set():
    player = basic_player()
    gear = GearSet()
    ring = ring_of_power()
    gear.equip("ring1", ring)

    total_modifiers = gear.get_total_modifiers(player)
    assert total_modifiers.strength == 30

    # Equip a second ring and test
    ring2 = ring_of_agility()
    gear.equip("ring2", ring2)

    total_modifiers = gear.get_total_modifiers(player)
    assert total_modifiers.strength == 30
    assert total_modifiers.agility == 5


def test_invalid_slot():
    gear = GearSet()
    ring = ring_of_power()
    with pytest.raises(ValueError):
        gear.equip("invalid_slot", ring)
