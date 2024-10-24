class MinesweeperAction:
    """
    a Minesweeper action takes a coordinate
    """
    __col: int
    __row: int

    def __init__(self, row: int, col: int):
        self.__col = col
        self.__row = row

    def get_col(self):
        return self.__col

    def get_row(self):
        return self.__row
