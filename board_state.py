from tkinter import Canvas, Event
from settings import Settings
from piece import *
import helpers


class BoardState:
    def __init__(self, canvas: Canvas, settings: Settings) -> None:
        self.settings = settings
        self.canvas = canvas
        # State variables
        self.is_picking = True
        self.turn = "w"
        self.click_position = None

        self.board_list = self.init_board()
        self.positions = self.create_positions()
        self.taken_pieces: dict[str, list[Piece]] = {"w": [], "b": []}

    def init_board(self) -> List[List[Union[None, "Piece"]]]:
        return [
            [
                Rock("b"),
                Knight("b"),
                Bishop("b"),
                Queen("b"),
                King("b"),
                Bishop("b"),
                Knight("b"),
                Rock("b"),
            ],
            [
                Pawn("b"),
                Pawn("b"),
                Pawn("b"),
                Pawn("b"),
                Pawn("b"),
                Pawn("b"),
                Pawn("b"),
                Pawn("b"),
            ],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [
                Pawn("w"),
                Pawn("w"),
                Pawn("w"),
                Pawn("w"),
                Pawn("w"),
                Pawn("w"),
                Pawn("w"),
                Pawn("w"),
            ],
            [
                Rock("w"),
                Knight("w"),
                Bishop("w"),
                Queen("w"),
                King("w"),
                Bishop("w"),
                Knight("w"),
                Rock("w"),
            ],
        ]

    def create_positions(self) -> list:
        sttgs = self.settings
        positions = []
        for row in range(8):
            for col in range(8):
                positions.append(
                    (
                        row * sttgs.sqr_size + sttgs.offset,
                        col * sttgs.sqr_size + sttgs.offset,
                        row * sttgs.sqr_size + sttgs.offset + sttgs.sqr_size,
                        col * sttgs.sqr_size + sttgs.offset + sttgs.sqr_size,
                        (col, row),
                    )
                )
        return positions

    def handle_click(self, event: Event) -> None:
        col = event.x
        row = event.y

        for x1, y1, x2, y2, pos in self.positions:
            if (col > x1 and col < x2) and (row > y1 and row < y2):
                self.handle_square(pos[0], pos[1], x1, y1)

    def toggle_turn(self) -> None:
        if self.turn == "w":
            self.turn = "b"
            self.canvas.itemconfig(
                tagOrId="white",
                fill=self.settings.WHITE_STATS,
                font=("Verdana", self.settings.label_size, "bold"),
            )
            self.canvas.itemconfig(
                tagOrId="black",
                fill=self.settings.BLACK,
                font=("Verdana", self.settings.label_size),
            )
        else:
            self.turn = "w"
            self.canvas.itemconfig(
                tagOrId="white",
                fill=self.settings.WHITE_STATS,
                font=("Verdana", self.settings.label_size),
            )
            self.canvas.itemconfig(
                tagOrId="black",
                fill=self.settings.BLACK,
                font=("Verdana", self.settings.label_size, "bold"),
            )

    def handle_square(self, row: int, col: int, x: int, y: int):
        if self.is_picking:
            self.piece: Piece = self.board_list[row][col]
            if self.piece is None or self.piece.color != self.turn:
                return
            self.click_position = (row, col)
            # light on
            self.valid_sqr = self.piece.valid_moves(row, col, self.board_list)
            helpers.lights_on(self.valid_sqr, self.canvas, self.settings)
            self.is_picking = False

        else:
            new_piece = self.board_list[row][col]
            if self.click_position is None:
                return
            if row == self.click_position[0] and col == self.click_position[1]:
                return
            # pick another piece in the same turn
            if new_piece is not None and new_piece.color == self.turn:
                helpers.lights_off(self.valid_sqr, self.canvas, self.settings)
                self.is_picking = True
                self.handle_square(row, col, x, y)
            # move the piece
            if (
                self.board_list[self.click_position[0]][self.click_position[1]]
                is not None
            ):
                if (row, col) in self.valid_sqr:
                    # Take a piece
                    if new_piece is not None and new_piece.color != self.turn:
                        self.taken_pieces[new_piece.color].append(new_piece)
                        helpers.show_taken(
                            canvas=self.canvas,
                            taken_pieces=self.taken_pieces,
                            sttgs=self.settings,
                        )
                    cpx, cpy = self.click_position
                    self.board_list[row][col] = self.board_list[cpx][cpy]
                    self.board_list[cpx][cpy] = None
                    self.canvas.coords(
                        self.piece.img_id,
                        x + self.settings.sqr_size // 2,
                        y + self.settings.sqr_size // 2,
                    )
                    self.board_list[row][col].has_moved = True
                    # Lights off
                    helpers.lights_off(self.valid_sqr, self.canvas, self.settings)
                    self.is_picking = True
                    self.click_position = None
                    self.toggle_turn()
