class StatModifierChain:

    def __init__(self, base_value):
        self.base_value = base_value
        self.modifiers = []


    def add_modifier(self, modifier_func):
        self.modifiers.append(modifier_func)

    def get_value(self):
        value = self.base_value
        for modifier in self.modifiers:
            value = modifier(value)  # Pass the current value to each modifier
        return value



class BasicStats:
    def __init__(self, **kwargs):
        self._specified_keys = set(kwargs.keys())  # Track only initialized attributes
        self.__dict__.update(kwargs)


    def __getattr__(self, name):
        # If the attribute isn't present, default to 0

        return 0

    def __dir__(self):
        # Return only the explicitly specified attributes
        return list(self._specified_keys)


class Player(BasicStats):
    def wearing(self, *items):
        return PlayerWearingStats(self, *items)



class PlayerWearingStats:
    def __init__(self, base_stats, *items):

        self.base_stats = base_stats
        self.items = items
        self.modifier_chains = {}


        # For each stat in the base player, create a modifier chain

        for stat in base_stats._specified_keys:
            self.modifier_chains[stat] = StatModifierChain(getattr(base_stats, stat))

        # Now, apply each item's buffs to the appropriate stats
        for item in items:
            for stat in dir(item):
                if stat not in self.modifier_chains:

                    self.modifier_chains[stat] = StatModifierChain(0)

                # Add the item's stat as a modifier function
                def modifier_func(base_value, inc=item, s=stat):
                    return base_value + getattr(inc, s)


                self.modifier_chains[stat].add_modifier(modifier_func)

    def __getattr__(self, name):
        if name in self.modifier_chains:
            # If we have a modifier chain for the stat, return the calculated value
            return self.modifier_chains[name].get_value()
        return 0

    def __dir__(self):
        return list(self.modifier_chains.keys())

