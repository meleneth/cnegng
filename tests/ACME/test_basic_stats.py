from flexmock import flexmock
import pygame

from cnegng.ACME import Player
from cnegng.ACME import BasicStats

def basic_player():
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
    return BasicStats(
        maximum_life = 10
    )

def test_basic_stats_are_basic():
    stats = basic_player()
    assert stats.maximum_life == 60

def test_basic_stats_dir_is_attributes_based():
    ring = small_vit_ring()
    assert dir(ring) == ['maximum_life']

def test_player_wearing_ring_is_buff():
    player = basic_player()
    ring = small_vit_ring()

    assert player.wearing(ring).maximum_life == 70

def test_player_if_ring_gets_better_we_notice():
    player = basic_player()
    ring = small_vit_ring()
 
    # oh sure, if we're accepting handwaves everything is fine
    # the joke here is that 'wearing' has the complexity needed to simulate toast
    active_stats = player.wearing(ring)
    assert active_stats.maximum_life == 70

    # so for this to work we need a custom gettattr right?
    setattr(ring, "maximum_life", 20)
    assert active_stats.maximum_life == 80

def test_two_rings_are_more_fun_than_one():
    player = basic_player()
    ring1 = small_vit_ring()
    ring2 = small_vit_ring()
 
    active_stats = player.wearing(ring1, ring2)
    assert active_stats.maximum_life == 80
