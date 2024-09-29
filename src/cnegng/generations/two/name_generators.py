import random

# Base NameGenerator class for shared functionality
class NameGenerator:
    def generate_name(self):
        raise NotImplementedError("Subclasses should implement this method")

# Elvish Name Generator
class ElvishNameGenerator(NameGenerator):
    def __init__(self):
        self.prefixes = ['Aer', 'Ela', 'Lia', 'Syl', 'Tia', 'Val', 'Cel', 'Faen', 'Gala', 'Irid', 'Isil', 'Loth', 'Nima', 'Quel', 'Vala']
        self.middles = ['an', 'iel', 'lin', 'mar', 'wen', 'ion', 'lis', 'nor', 'wyn', 'riel']
        self.suffixes = ['anor', 'iel', 'eth', 'wyn', 'dar', 'ith', 'len', 'thor', 'mir', 'dor']

    def generate_name(self):
        prefix = random.choice(self.prefixes)
        suffix = random.choice(self.suffixes)
        
        if random.random() > 0.5:
            middle = random.choice(self.middles)
            return prefix + middle + suffix
        else:
            return prefix + suffix

# Orcish Name Generator
class OrcishNameGenerator(NameGenerator):
    def __init__(self):
        self.prefixes = ['Gor', 'Thok', 'Morg', 'Rok', 'Dur', 'Zug', 'Krag', 'Ugl', 'Grim', 'Nar', 'Brak', 'Drok', 'Urk', 'Kro']
        self.middles = ['gar', 'mak', 'thok', 'zug', 'krag', 'drok', 'nash', 'burz', 'shak', 'ug']
        self.suffixes = ['gash', 'thar', 'zug', 'nak', 'drok', 'mak', 'zog', 'ruk', 'gorn', 'zash']

    def generate_name(self):
        prefix = random.choice(self.prefixes)
        suffix = random.choice(self.suffixes)
        
        if random.random() > 0.5:
            middle = random.choice(self.middles)
            return prefix + middle + suffix
        else:
            return prefix + suffix
