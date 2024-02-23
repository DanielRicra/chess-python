import tkinter
from board_state import BoardState
from board_graphic import BoardGraphic
from piece import Piece
from settings import Settings
from PIL import ImageTk


class BoardGraphicImpl(BoardGraphic):
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

        self.root = tkinter.Tk()
        self.canvas = tkinter.Canvas(
            self.root,
            width=self.settings.canvas_width,
            height=self.settings.canvas_height,
        )
        self.canvas.pack()

        self.board_state = BoardState(canvas=self.canvas, settings=self.settings)
        self.board_list = self.board_state.board_list
        self.play_again_img = ImageTk.PhotoImage(file="./assets/play-again.png")

        self.init_draw()

    def draw_stats(self, x1: int, y1: int, x2: int, y2: int):
        self.canvas.create_rectangle(x1, y1, x2, y2)
        self.canvas.create_text(
            x1 + self.settings.label_size * 2.5,
            self.settings.offset,
            fill=self.settings.BLACK,
            font=("Verdana", self.settings.label_size),
            tags="black",
            text="Black",
        )
        self.canvas.create_text(
            x1 + self.settings.label_size * 2.5,
            y2 - self.settings.offset + 0.4 * self.settings.offset,
            fill=self.settings.WHITE_STATS,
            font=("Verdana", self.settings.label_size, "bold"),
            tags="white",
            text="White",
        )

    def init_draw(self):
        sttgs = self.settings
        bottom = sttgs.board_size + sttgs.label_size * 3
        self.canvas.create_rectangle(
            (sttgs.label_size, sttgs.label_size), (bottom, bottom)
        )
        self.canvas.create_rectangle(
            (sttgs.offset, sttgs.offset),
            (bottom - sttgs.label_size, bottom - sttgs.label_size),
        )

        for row in range(8):
            for col in range(8):
                color = sttgs.BLACK if self.is_black_cell(row, col) else sttgs.WHITE
                x = sttgs.offset + (sttgs.sqr_size * col)
                y = sttgs.offset + (sttgs.sqr_size * row)
                self.canvas.create_rectangle(
                    (x, y),
                    (x + sttgs.sqr_size, y + sttgs.sqr_size),
                    fill=color,
                    tags=f"{row},{col}",
                    outline="",
                )

        letters = ["a", "b", "c", "d", "e", "f", "g", "h"]
        for n in range(1, 9):
            step = sttgs.offset + (sttgs.sqr_size * n) - (sttgs.sqr_size // 2)
            self.canvas.create_text(
                (sttgs.label_size * 1.5, step),
                text=str(n),
            )
            self.canvas.create_text(
                (
                    step,
                    sttgs.offset + (sttgs.label_size / 2) + sttgs.board_size,
                ),
                text=letters[n - 1],
            )

        # Set the pieces
        for row in range(8):
            for col in range(8):
                piece: Piece | None = self.board_list[row][col]
                if piece is not None:
                    image = piece.piece_img()
                    piece_image = self.canvas.create_image(
                        sttgs.offset + (col * sttgs.sqr_size) + sttgs.sqr_size // 2,
                        sttgs.offset + (row * sttgs.sqr_size) + sttgs.sqr_size // 2,
                        image=image,
                    )
                    piece.img_id = piece_image
        self.draw_stats(
            sttgs.board_size + sttgs.offset * 2,
            sttgs.label_size,
            sttgs.board_size * 3 + sttgs.sqr_size * 5,
            sttgs.board_size + sttgs.label_size * 3,
        )

    def is_black_cell(self, row, col) -> bool:
        return col % 2 != 0 and row % 2 == 0 or row % 2 != 0 and col % 2 == 0

    def mainloop(self):
        tkinter.mainloop()

    def set_new_game(self):
        self.canvas.delete("all")
        self.board_state.is_picking = True
        self.board_state.turn = "w"
        self.board_state.click_position = None
        self.board_state.taken_pieces = {"w": [], "b": []}
        self.board_list = self.board_state.init_board()
        self.init_draw()
        self.board_state.board_list = self.board_list
        self.play_again.destroy()

    def end_game(self):
        self.play_again = tkinter.Button(
            self.root, image=self.play_again_img, border=0, command=self.set_new_game
        )
        self.play_again.place(
            x=self.settings.board_size * 5 // 4,
            y=self.settings.board_size // 2 + self.settings.offset,
        )
