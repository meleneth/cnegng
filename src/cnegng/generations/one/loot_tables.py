from cnegng.ACME import LootTable
from cnegng.generations.one.items import small_vit_ring, percent_life_ring, boss_helm


def basic_loot_table():
    drops = LootTable()
    drops.add_entry(1 / 4, lambda: small_vit_ring())
    drops.add_entry(1 / 32, lambda: percent_life_ring())
    return drops


def boss_loot_table():
    basic_loot = basic_loot_table()
    drops = LootTable()
    drops.add_entry(1 / 2, lambda: boss_helm())
    basic_loot.copy_loot_to(drops)
    return drops
