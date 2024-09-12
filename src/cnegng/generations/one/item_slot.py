from typing import List, Dict, Any, Optional


from cnegng.ACME.stats.item_with_modifiers import ItemWithModifiers


class ItemSlot:
    """
    Represents a slot in which an item can be equipped.

    Attributes
    ----------
    name : str
        The name of the slot (e.g., 'ring', 'amulet').
    item : Optional[ItemWithModifiers]
        The item equipped in this slot, if any.
    """

    def __init__(self, name: str) -> None:
        """
        Parameters
        ----------
        name : str
            The name of the slot (e.g., 'ring', 'amulet').
        """
        self.name: str = name
        self.item: Optional[ItemWithModifiers] = None

    def equip_item(self, item: ItemWithModifiers) -> None:
        """
        Equip an item into the slot.

        Parameters
        ----------
        item : ItemWithModifiers
            The item to equip.
        """
        self.item = item

    def unequip_item(self) -> None:
        """
        Unequip the current item from the slot.
        """
        self.item = None

    def get_modifiers(self) -> Dict[str, float]:
        """
        Get the stat modifiers from the item in this slot.

        Returns
        -------
        Dict[str, float]
            The modifiers from the equipped item, or an empty dictionary if no item is equipped.
        """
        return self.item.modifiers if self.item else {}
