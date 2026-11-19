"""Ball position and safe step movement."""


class Ball:
    """A circular ball whose complete bounds stay inside its window."""

    RADIUS = 25
    STEP = 20

    def __init__(self, x: int, y: int, width: int, height: int):
        self.x, self.y = x, y
        self.width, self.height = width, height

    def move(self, dx: int, dy: int) -> None:
        """Apply a step only when the resulting circle remains on screen."""
        next_x, next_y = self.x + dx, self.y + dy
        if (self.RADIUS <= next_x <= self.width - self.RADIUS and
                self.RADIUS <= next_y <= self.height - self.RADIUS):
            self.x, self.y = next_x, next_y
