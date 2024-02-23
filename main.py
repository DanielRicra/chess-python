from chess import BoardGraphicImpl
from settings import Settings


def main():
    chess_settings = Settings()
    chess = BoardGraphicImpl(chess_settings)
    chess.canvas.bind("<Button-1>", chess.board_state.handle_click)  # left click
    chess.mainloop()


if __name__ == "__main__":
    main()
