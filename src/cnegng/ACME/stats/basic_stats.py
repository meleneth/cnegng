class BasicStats:
    def __init__(self, **kwargs):
        """
        Initializes a BasicStats object with arbitrary keyword arguments as attributes. Each attribute corresponds
        to a stat like 'maximum_life', 'strength', etc.

        :param kwargs: Arbitrary stats provided as keyword arguments (e.g., maximum_life=60, strength=10).
        """
        self._specified_keys = set(kwargs.keys())  # Track only initialized attributes
        self.__dict__.update(kwargs)

    def __dir__(self):
        """

        Returns only the explicitly specified attributes in the object.

        :return: A list of the stat names that were explicitly initialized.
        """

        return list(self._specified_keys)
