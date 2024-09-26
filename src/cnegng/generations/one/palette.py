# Color palette (limited to a few colors)
def vibrant():
    return [
        (255, 99, 71),  # Tomato
        (135, 206, 235),  # SkyBlue
        (152, 251, 152),  # PaleGreen
        (255, 182, 193),  # LightPink
        (255, 255, 0),  # Yellow
        (255, 165, 0),  # Orange
        (173, 216, 230),  # LightBlue
        (240, 128, 128),  # LightCoral
        (124, 252, 0),  # LawnGreen
        (255, 69, 0),  # OrangeRed
    ]

def without_red(palette):
    return [[0, g, b] for (r, g, b) in palette]
