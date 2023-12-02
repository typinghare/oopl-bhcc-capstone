"""
Common module.
"""
from typing import Tuple, List, Any

from pygame import Rect


class Size:
    """
    A size where width and height are constant integers.
    """

    def __init__(self, width: int, height: int):
        self._width = width
        self._height = height

    @property
    def width(self):
        """
        Returns the width of this size.
        """
        return self._width

    @property
    def height(self):
        """
        Returns the height of this size.
        """
        return self._height

    def toTuple(self) -> Tuple[int, int]:
        """
        Converts this size to a tuple.
        """
        return self._width, self._height

    def __mul__(self, other: "Size"):
        """
        Multiplies two sizes.
        :param other: The other size to multiply.
        :return: A new size.
        """
        return Size(self._width * other._width, self._height * other._height)


class ListWrapper:
    """
    List wrapper. (In python, lists cannot be hashed)
    """

    def __init__(self, list_to_wrap: List[Any]):
        self.list = list_to_wrap


class Grid:
    """
    General grid.
    """

    def __init__(self, size: Size, cell: Any = None):
        # The size of this grid
        self.size = size

        # Cells
        self._cells: List[Any] = [None] * size.width * size.height

        # Fill
        if cell is not None:
            self.fill(cell)

    def get_index(self, coordinate: Tuple[int, int]) -> Any:
        """
        Gets the index of a coordinate (x = col, y = row).
        :param coordinate: The coordinate to get the index of.
        """
        return coordinate[1] * self.size.width + coordinate[0]

    def get(self, coordinate: Tuple[int, int]) -> Any:
        """
        Retrieves a cell.
        :param coordinate: The coordinate of the cell to retrieve.
        :return: The cell at the specified coordinate (or index).
        """
        return self._cells[self.get_index(coordinate)]

    def set(self, coordinate: Tuple[int, int], cell: Any) -> None:
        """
        Sets a cell.
        :param coordinate: The coordinate of the cell to set.
        :param cell: The cell to set.
        """
        self._cells[self.get_index(coordinate)] = cell

    def fill(self, cell: Any) -> None:
        """
        Fills all cells with a given value.
        :param cell: The value of fill.
        """
        for i in range(0, len(self._cells)):
            self._cells[i] = cell

    def __getitem__(self, index: int) -> Any:
        """
        Retrieves a cell of a specified index.
        :param index: The index of the cell to retrieve.
        """
        return self._cells[index]

    def __setitem__(self, index: int, cell: Any) -> None:
        """
        Sets the value of a cell.
        :param index: The index of the cell.
        :param cell: The cell to set.
        """
        self._cells[index] = cell

    def __len__(self) -> int:
        """
        Returns the size of cells.
        """
        return len(self._cells)

    def get_iterator(
        self, row_range: Tuple[int, int], col_range: Tuple[int, int]
    ) -> "Grid.Iterator":
        """
        Returns an iterator.
        :param row_range: The range of row.
        :param col_range: The range of column.
        """
        return self.Iterator(self, row_range, col_range)

    class Iterator:
        """
        Grid iterator.
        """

        def __init__(self, grid: "Grid", row_range: Tuple[int, int], col_range: Tuple[int, int]):
            self.grid = grid
            self.row_start, self.row_end = row_range
            self.col_start, self.col_end = col_range
            self.current_row = self.row_start
            self.current_col = self.col_start

        def __iter__(self):
            return self

        def __next__(self):
            if self.current_row >= self.row_end:
                raise StopIteration

            cell = self.grid.get((self.current_col, self.current_row))
            self.current_col += 1

            if self.current_col >= self.col_end:
                self.current_col = self.col_start
                self.current_row += 1

            return cell


class CoordinateSet:
    """
    Coordinate set allows adding and checking, but does not allow remove.
    """

    def __init__(self):
        self._coordinate_set: set = set()

    @staticmethod
    def from_rect(rect: Rect) -> "CoordinateSet":
        """
        Converts a rectangle to a coordinate set.
        """
        coordinate_set = CoordinateSet()
        for row in range(rect.y, rect.y + rect.height):
            for col in range(rect.x, rect.x + rect.width):
                coordinate_set.add((col, row))

        return coordinate_set

    def add(self, coordinate: Tuple[int, int]) -> None:
        """
        Adds a coordinate
        :param coordinate: The coordinate to add.
        """
        self._coordinate_set.add(coordinate)

    def has(self, coordinate: Tuple[int, int]) -> bool:
        """
        Checks whether a given coordinate is in the set.
        :param coordinate: The coordinate to check.
        """
        return coordinate in self._coordinate_set

    def remove(self, coordinate: Tuple[int, int]) -> None:
        """
        Removes a coordinate
        """
        self._coordinate_set.remove(coordinate)

    def all(self) -> set:
        """
        Returns all coordinates.
        """
        return self._coordinate_set
