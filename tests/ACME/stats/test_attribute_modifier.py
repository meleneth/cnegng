from flexmock import flexmock
import pygame

from cnegng.ACME import AttributeModifier

def test_attribute_modifier():
    attribute_modifier = AttributeModifier("maximum_life", "percent", 0.5)
