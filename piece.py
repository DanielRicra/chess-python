from PIL import Image, ImageTk
from typing import List, Union


class Piece:
    def __init__(self, color: str) -> None:
        self.color = color
        self.img_id = None
        self.has_moved = False

        self.path = ""

    def piece_img(self, img_size: int = 50):
        img = Image.open(self.path)
        # img = img.resize((img_size, img_size)) # if want to resize the image
        self.piece_image = ImageTk.PhotoImage(img)
        return self.piece_image

    def check_range(self, row: int, col: int) -> bool:
        if row > 7 or row < 0 or col > 7 or col < 0:
            return False
        return True

    def can_move(
        self, row: int, col: int, board_list: List[List[Union[None, "Piece"]]]
    ):
        if self.check_range(row, col):
            if board_list[row][col] is None:
                return True
            if board_list[row][col].color != self.color:
                return True
        return False

    def valid_moves(
        self, row: int, col: int, board_list: List[List[Union[None, "Piece"]]]
    ) -> list[(int, int)]:
        pass


class Pawn(Piece):
    def __init__(self, color: str) -> None:
        super().__init__(color)
        self.path = f"./assets/{color}p.png"

    def valid_moves(
        self, row: int, col: int, board_list: List[List[Union[None, "Piece"]]]
    ) -> list[(int, int)]:
        res = []
        if self.color == "w":
            if board_list[row - 1][col] is None:
                res.append((row - 1, col))
            if (col - 1 > 0 and board_list[row - 1][col - 1] is not None) and (
                board_list[row - 1][col - 1].color != self.color
            ):
                res.append((row - 1, col - 1))
            if (col + 1 < 8 and board_list[row - 1][col + 1] is not None) and (
                board_list[row - 1][col + 1].color != self.color
            ):
                res.append((row - 1, col + 1))
            if self.has_moved == False and (
                board_list[row - 1][col] is None and board_list[row - 2][col] is None
            ):
                res.append((row - 2, col))
        else:
            if board_list[row + 1][col] is None:
                res.append((row + 1, col))
            if (col - 1 > 0 and board_list[row + 1][col - 1] is not None) and (
                board_list[row + 1][col - 1].color != self.color
            ):
                res.append((row + 1, col - 1))
            if (col + 1 < 8 and board_list[row + 1][col + 1] is not None) and (
                board_list[row + 1][col + 1].color != self.color
            ):
                res.append((row + 1, col + 1))
            if self.has_moved == False and (
                board_list[row + 1][col] is None and board_list[row + 2][col] is None
            ):
                res.append((row + 2, col))
        return res


class Rock(Piece):
    def __init__(self, color: str) -> None:
        super().__init__(color)
        self.path = f"./assets/{color}r.png"

    def valid_moves(
        self, row: int, col: int, board_list: List[List[Union[None, "Piece"]]]
    ) -> list[(int, int)]:
        res = []
        directions = [(0, -1), (0, 1), (1, 0), (-1, 0)]
        for x, y in directions:
            for step in range(1, 8):
                new_row = row + (step * x)
                new_col = col + (step * y)
                if self.can_move(new_row, new_col, board_list):
                    res.append((new_row, new_col))
                    if (
                        board_list[new_row][new_col] != None
                        and board_list[new_row][new_col].color != self.color
                    ):
                        break
                else:
                    break
        return res


class Bishop(Piece):
    def __init__(self, color: str) -> None:
        super().__init__(color)
        self.path = f"./assets/{color}b.png"

    def valid_moves(
        self, row: int, col: int, board_list: List[List[Union[None, "Piece"]]]
    ) -> list[(int, int)]:
        res = []
        directions = [
            (1, -1),
            (-1, -1),
            (-1, 1),
            (1, 1),
        ]
        for x, y in directions:
            for step in range(1, 8):
                new_row = row + (step * x)
                new_col = col + (step * y)
                if self.can_move(new_row, new_col, board_list):
                    res.append((new_row, new_col))
                    if (
                        board_list[new_row][new_col] != None
                        and board_list[new_row][new_col].color != self.color
                    ):
                        break
                else:
                    break
        return res


class Knight(Piece):
    def __init__(self, color: str) -> None:
        super().__init__(color)
        self.path = f"./assets/{color}n.png"

    def valid_moves(
        self, row: int, col: int, board_list: List[List[Union[None, "Piece"]]]
    ) -> list[(int, int)]:
        res = []
        directions = [
            (1, -2),
            (-1, -2),
            (2, -1),
            (-2, -1),
            (-1, 2),
            (1, 2),
            (2, 1),
            (-2, 1),
        ]
        for x, y in directions:
            if self.can_move(row + x, col + y, board_list):
                res.append((row + x, col + y))
        return res


class Queen(Piece):
    def __init__(self, color: str) -> None:
        super().__init__(color)
        self.path = f"./assets/{color}q.png"

    def valid_moves(
        self, row: int, col: int, board_list: List[List[Union[None, "Piece"]]]
    ) -> list[(int, int)]:
        res = []
        directions = [
            (0, -1),
            (0, 1),
            (1, 0),
            (-1, 0),
            (1, -1),
            (-1, 1),
            (-1, -1),
            (1, 1),
        ]
        print(row, col)
        for x, y in directions:
            for step in range(1, 8):
                new_row = row + (step * x)
                new_col = col + (step * y)
                if new_row > 7 or new_col > 7:
                    continue
                piece: Piece | None = board_list[new_row][new_col]
                if self.can_move(new_row, new_col, board_list):
                    res.append((new_row, new_col))
                    if piece is not None and piece.color != self.color:
                        break
                else:
                    break
        return res


class King(Piece):
    def __init__(self, color: str) -> None:
        super().__init__(color)
        self.path = f"./assets/{color}k.png"

    def valid_moves(
        self, row: int, col: int, board_list: List[List[Union[None, "Piece"]]]
    ) -> list[(int, int)]:
        res = []
        directions = [
            (0, -1),
            (0, 1),
            (1, 0),
            (-1, 0),
            (1, -1),
            (-1, -1),
            (-1, 1),
            (1, 1),
        ]
        for x, y in directions:
            if self.can_move(row + x, col + y, board_list):
                res.append((row + x, col + y))
        return res
