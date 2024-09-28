import math

from cnegng.ACME.spatial2d.position import Position

class Circle:
    def __init__(self, center: Position, radius: float):
        self.center = center
        self.radius = radius

    def __repr__(self):
        return f"Circle(center={self.center}, radius={self.radius})"

    def contains_position(self, position: Position) -> bool:
        # Calculate the distance between the center of the circle and the position
        distance = math.sqrt((position.x - self.center.x) ** 2 + (position.y - self.center.y) ** 2)
        
        # Check if the distance is less than or equal to the radius
        return distance <= self.radius

    def move_along_arc(self, position, speed, dt):
        # Get the center coordinates
        C_x, C_y = self.center.x, self.center.y
        
        # Get current position coordinates
        x, y = position.x, position.y
        
        # Calculate the current relative radius (distance from center)
        relative_radius = math.sqrt((x - C_x) ** 2 + (y - C_y) ** 2)
        
        # Calculate the current angle theta (in radians) relative to the center
        theta = math.atan2(y - C_y, x - C_x)
        
        # Calculate angular displacement (arc length / relative radius)
        distance = speed * dt
        delta_theta = distance / relative_radius
        
        # Update the angle
        theta_new = theta + delta_theta
        
        # Calculate new position coordinates, maintaining the relative radius
        x_new = C_x + relative_radius * math.cos(theta_new)
        y_new = C_y + relative_radius * math.sin(theta_new)
        
        # Return new position as a Position object
        return Position(x_new, y_new)
