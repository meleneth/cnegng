from flexmock import flexmock
import pygame

from cnegng.ACME import Player
from cnegng.ACME import BasicStats, ItemWithModifiers, AttributeModifier

# Helper functions

def basic_player():
    """
    Creates a basic player with 60 maximum life.
    
    :return: A Player object with 'maximum_life' set to 60.
    """
    return Player(
        intelligence = 20,
        dexterity = 20,
        strength = 20,
        level = 1,
        life = 60,
        maximum_life = 60,
        mana = 50,
        maximum_mana = 50,
        fire_resistance = 0,
        cold_resistance = 0,
        lightning_resistance = 0,
        chaos_resistance = 0,
    )

def small_vit_ring():
    """

    Creates a ring that adds a flat +20 to 'maximum_life'.

    
    :return: An ItemWithModifiers object with a +20 'flat' modifier to 'maximum_life'.

    """
    return ItemWithModifiers([AttributeModifier('maximum_life', 'flat', 20)])

def percent_life_ring():
    """
    Creates a ring that increases 'maximum_life' by 50% (1.5x multiplier).
    

    :return: An ItemWithModifiers object with a 50% 'percent' modifier to 'maximum_life'.
    """
    return ItemWithModifiers([AttributeModifier('maximum_life', 'percent', 0.5)])

# Example Test Cases

def test_basic_stats_dir_is_attributes_based():
    ring = small_vit_ring()
    assert dir(ring) == ['maximum_life']

def test_player_wearing_ring_is_buff():

    player = basic_player()
    ring = small_vit_ring()

    assert player.wearing(ring).maximum_life == 80  # 60 base + 20 ring


def test_player_if_ring_gets_better_we_notice():
    player = basic_player()
    ring = small_vit_ring()


    active_stats = player.wearing(ring)

    assert active_stats.maximum_life == 80  # 60 base + 20 ring

    # Update the ring's maximum_life, and the player's active stats should reflect this immediately
    setattr(ring, "maximum_life", 20)
    assert active_stats.maximum_life == 80

def test_wearing_two_vit_rings():
    player = basic_player()
    ring1 = small_vit_ring()

    ring2 = small_vit_ring()

    active_stats = player.wearing(ring1, ring2)
    assert active_stats.maximum_life == 100  # 60 base + 20 + 20

def test_wearing_percentage_ring():
    player = basic_player()
    ring = percent_life_ring()


    active_stats = player.wearing(ring)

    assert active_stats.maximum_life == 90  # 60 base * 1.5

def test_wearing_flat_and_percentage_ring():
    player = basic_player()
    ring_flat = small_vit_ring()
    ring_percent = percent_life_ring()

    active_stats = player.wearing(ring_flat, ring_percent)

    assert active_stats.maximum_life == 120  # (60 base + 20 flat) * 1.5 = 120

