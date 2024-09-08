class StatModifierChain:

    def __init__(self, base_value):
        """
        Initializes a chain of stat modifiers starting from a base value.

        :param base_value: The base value of the stat before any modifiers are applied.
        """
        self.base_value = base_value
        self.modifiers = []

    def add_modifier(self, modifier_func):
        """
        Adds a new modifier function to the chain. Each modifier function should accept a base value and return
        the modified value.


        :param modifier_func: A function that takes the base value and modifies it.
        """
        self.modifiers.append(modifier_func)

    def get_value(self):
        """

        Calculates the final stat value after applying all the modifiers in the chain.

        :return: The modified stat value.
        """
        value = self.base_value

        for modifier in self.modifiers:
            value = modifier(value)  # Apply each modifier in the chain
        return value
