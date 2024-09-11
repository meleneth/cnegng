from cnegng.generations.one.items import small_vit_ring


def test_item_with_modifiers():
    ring = small_vit_ring()
    assert ring.modifiers[0].stat_name == "maximum_life"
    assert ring.modifiers[0].value == 20
