"""Visual theme constants: colors, fonts and icon tints."""

# Colors
ACCENT: str = "#1f538d"  # enabled button
DISABLED: str = "#525252"  # disabled button
HIST_BG: str = "#242424"  # matplotlib histogram background

# Fonts
PLACEHOLDER_FONT: tuple[str, int, str] = ("Arial", 13, "italic")
PLACEHOLDER_TEXT_COLOR: str = "gray"

# Tint colors for monochrome placeholder icons, per appearance mode.
# Light gray for dark backgrounds, darker gray for light backgrounds.
LIGHT_TINT: tuple[int, int, int] = (110, 110, 110)
DARK_TINT: tuple[int, int, int] = (160, 160, 160)
