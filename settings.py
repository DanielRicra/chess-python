class Settings:
    """Stores all the setting of chess game."""

    def __init__(self) -> None:
        """Initialize the game's static settings"""
        self.sqr_size = 50
        self.label_size = (self.sqr_size // 10) * 2
        self.offset = self.label_size * 2
        self.board_size = self.sqr_size * 8
        # Tkinter Canvas
        self.canvas_width = self.board_size + self.offset * 2 + self.sqr_size * 5
        self.canvas_height = self.board_size + self.offset * 2
        # Colors
        self.WHITE = "#E7E6E1"
        self.BLACK = "#4b7399"
        self.WHITE_STATS = "#F28268"
        self.LIGHT_WHITE = "#b3b3b3"
        self.LIGHT_BLACK = "#34506b"
