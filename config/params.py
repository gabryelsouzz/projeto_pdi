"""Parameter ranges and defaults for the image transformations."""

THRESHOLD_RANGE: tuple[int, int] = (0, 255)
THRESHOLD_DEFAULT: int = 128

C_RANGE: tuple[float, float] = (0.0, 3.0)
C_DEFAULT: float = 1.0

B_RANGE: tuple[int, int] = (-255, 255)
B_DEFAULT: int = 0
