from cnegng.ACME import PlayerWearingStats
from cnegng.generations.one import basic_player, small_vit_ring, percent_life_ring


def test_basic_stats_dir_is_attributes_based():
    ring = small_vit_ring()
    assert dir(ring) == ["maximum_life"]


def test_PlayerWearingStats_wearing_nothing_is_fine():
    player = basic_player()
    dynamic_stats = PlayerWearingStats(player)
    assert dynamic_stats.maximum_life == 60  # 60 base


def test_PlayerWearingStats_ring_is_buff():
    player = basic_player()
    ring = small_vit_ring()
    dynamic_stats = PlayerWearingStats(player, ring)
    assert dynamic_stats.maximum_life == 80  # 60 base + 20 ring


def test_player_if_ring_gets_better_we_notice():
    player = basic_player()
    ring = small_vit_ring()
    active_stats = PlayerWearingStats(player, ring)
    assert active_stats.maximum_life == 80  # 60 base + 20 ring
    # Update the ring's maximum_life, and the player's active stats should reflect this immediately
    ring.modifiers[0].value = 40
    assert active_stats.maximum_life == 100


def test_player_if_player_gets_better_we_notice():
    player = basic_player()
    ring = small_vit_ring()
    active_stats = PlayerWearingStats(player, ring)
    assert active_stats.maximum_life == 80  # 60 base + 20 ring
    # Update the player's maximum_life, and the player's active stats should reflect this immediately
    setattr(player, "maximum_life", 200)
    assert active_stats.maximum_life == 220


def test_wearing_two_vit_rings():
    player = basic_player()
    ring1 = small_vit_ring()
    ring2 = small_vit_ring()
    active_stats = PlayerWearingStats(player, ring1, ring2)
    assert active_stats.maximum_life == 100  # 60 base + 20 + 20


def test_wearing_percentage_ring():
    player = basic_player()
    ring = percent_life_ring()
    active_stats = PlayerWearingStats(player, ring)
    assert active_stats.maximum_life == 90  # 60 base * 1.5


def test_wearing_flat_and_percentage_ring():
    player = basic_player()
    ring_flat = small_vit_ring()
    ring_percent = percent_life_ring()
    active_stats = PlayerWearingStats(player, ring_flat, ring_percent)
    assert active_stats.maximum_life == 120  # (60 base + 20 flat) * 1.5 = 120
