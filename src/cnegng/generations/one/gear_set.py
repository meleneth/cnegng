from typing import List, Dict, Any, Optional

from cnegng.generations.one.item_slot import ItemSlot
from cnegng.ACME.stats.item_with_modifiers import ItemWithModifiers
from cnegng.ACME.stats.player_wearing_stats import PlayerWearingStats


class GearSet:
    """
    Represents a full gear set, with various item slots.

    Attributes
    ----------
    slots : Dict[str, ItemSlot]
        A dictionary of gear slots.
    """

    def __init__(self) -> None:
        """
        Initializes all available slots in the gear set.
        """
        self.slots: Dict[str, ItemSlot] = {
            "ring1": ItemSlot("ring1"),
            "ring2": ItemSlot("ring2"),
            "amulet": ItemSlot("amulet"),
            "boots": ItemSlot("boots"),
            "pants": ItemSlot("pants"),
            "chest": ItemSlot("chest"),
            "shoulders": ItemSlot("shoulders"),
            "cape": ItemSlot("cape"),
            "helmet": ItemSlot("helmet"),
            "gloves": ItemSlot("gloves"),
        }

    def equip(self, slot_name: str, item: ItemWithModifiers) -> None:
        """
        Equip an item in a specified slot.

        Parameters
        ----------
        slot_name : str
            The name of the slot to equip the item in.
        item : ItemWithModifiers
            The item to equip in the slot.
        """
        if slot_name in self.slots:
            self.slots[slot_name].equip_item(item)
        else:
            raise ValueError(f"Invalid slot: {slot_name}")

    def unequip(self, slot_name: str) -> None:
        """
        Unequip the item from a specified slot.

        Parameters
        ----------
        slot_name : str
            The name of the slot to unequip the item from.
        """
        if slot_name in self.slots:
            self.slots[slot_name].unequip_item()
        else:
            raise ValueError(f"Invalid slot: {slot_name}")

    def get_total_modifiers(self, base_stats):
        return PlayerWearingStats(
            base_stats,
            *self.equipped_items(),
        )

    def equipped_items(self):
        return [slot.item for slot in self.slots.values() if slot.item is not None]
