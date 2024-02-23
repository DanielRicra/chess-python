from typing import List, Tuple
from tkinter import Canvas
from settings import Settings
from piece import *


def lights_on(validSqr: List[Tuple[int, int]], canvas: Canvas, sttgs: Settings):
    for row, col in validSqr:
        color = canvas.itemcget(f"{row},{col}", "fill")
        if color == sttgs.WHITE:
            canvas.itemconfig(tagOrId=f"{row},{col}", fill=sttgs.LIGHT_WHITE)
        else:
            canvas.itemconfig(tagOrId=f"{row},{col}", fill=sttgs.LIGHT_BLACK)


def lights_off(validSqr: List[Tuple[int, int]], canvas: Canvas, sttgs: Settings):
    for row, col in validSqr:
        color = canvas.itemcget(f"{row},{col}", "fill")
        if color == sttgs.LIGHT_WHITE:
            canvas.itemconfig(tagOrId=f"{row},{col}", fill=sttgs.WHITE)
        else:
            canvas.itemconfig(tagOrId=f"{row},{col}", fill=sttgs.BLACK)


def show_taken(
    canvas: Canvas, taken_pieces: dict[str, list[Piece]], sttgs: Settings
) -> None:
    b_row_counter = -1
    for i, piece in enumerate(taken_pieces["b"]):
        if i % 7 == 0:
            b_row_counter += 1

        x = sttgs.board_size + sttgs.sqr_size * 1.2 + (i % 7) * (sttgs.sqr_size * 0.65)
        y = (5.5 + b_row_counter) * sttgs.sqr_size + sttgs.label_size
        canvas.coords(piece.img_id, x, y)

    w_row_counter = -1
    for i, piece in enumerate(taken_pieces["w"]):
        if i % 7 == 0:
            w_row_counter += 1

        x = sttgs.board_size + sttgs.sqr_size * 1.2 + (i % 7) * (sttgs.sqr_size * 0.65)
        y = sttgs.offset * 2.5 + w_row_counter * sttgs.sqr_size
        canvas.coords(piece.img_id, x, y)
