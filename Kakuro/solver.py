from dataclasses import dataclass, field
from typing import Optional, Dict, Any
import json

BOARD_ROWS = 9
BOARD_COLS = 9


class Cell:
    """Clase base para las celdas del tablero."""

    def is_blocked(self) -> bool:
        return False

    def is_clue(self) -> bool:
        return False

    def is_empty(self) -> bool:
        return False


@dataclass
class BlockedCell(Cell):
    def is_blocked(self) -> bool:
        return True


@dataclass
class ClueCell(Cell):
    right: Optional[int] = None
    down: Optional[int] = None

    def is_clue(self) -> bool:
        return True


@dataclass
class EmptyCell(Cell):
    value: Optional[int] = None

    def is_empty(self) -> bool:
        return True

    def set_value(self, val: Optional[int]) -> None:
        self.value = val


@dataclass
class Board:
    cells: Dict[str, Cell] = field(default_factory=dict)

    def get_cell(self, coord: str) -> Cell:
        """Obtiene una celda dado su coordenada. Devuelve BlockedCell si no existe."""
        return self.cells.get(coord, BlockedCell())

    def set_cell(self, coord: str, cell: Cell) -> None:
        self.cells[coord] = cell

    def load_from_json(self, json_data: Dict[str, Any]) -> None:
        """Carga el tablero desde un diccionario JSON."""

        for row in range(BOARD_ROWS):
            for col in range(1, BOARD_COLS + 1):
                coord = f"{chr(ord('A') + row)}{col}"
                self.cells[coord] = EmptyCell()

        for coord, data in json_data.items():
            if data.get("blockedCell") is True:
                self.cells[coord] = BlockedCell()
            elif clue := data.get("clueCell"):
                right = clue.get("right")
                down = clue.get("down")
                self.cells[coord] = ClueCell(right=right, down=down)
            elif value := data.get("value"):

                if isinstance(value, int):
                    self.cells[coord] = EmptyCell(value=value)

    def display(self) -> None:
        """Imprime el tablero formateado usando ASCII para el marco."""

        print("     " + "   ".join(chr(ord("A") + i) for i in range(BOARD_COLS)))
        print("   ┌" + "───┬" * (BOARD_COLS - 1) + "───┐")

        for row in range(BOARD_ROWS):
            row_letter = chr(ord("A") + row)
            row_number = f"{row + 1:>2}"

            l1, l2, l3 = [], [], []

            for col in range(1, BOARD_COLS + 1):
                coord = f"{row_letter}{col}"
                cell: Cell = self.get_cell(coord)

                if cell.is_blocked():
                    l1.append("███")
                    l2.append("███")
                    l3.append("███")
                elif cell.is_clue():
                    right = f"{cell.right:0>2}" if cell.right is not None else "  "
                    down = f"{cell.down:0>2}" if cell.down is not None else "  "
                    l1.append(f"\\{right}")
                    l2.append(" \\ ")
                    l3.append(f"{down}\\")
                elif cell.is_empty():
                    val = str(cell.value) if cell.value is not None else " "
                    l1.append("   ")
                    l2.append(f" {val} ")
                    l3.append("   ")
                else:
                    l1.append("???")
                    l2.append("???")
                    l3.append("???")

            print(f"{row_number} │" + "│".join(l1) + "│")
            print("   │" + "│".join(l2) + "│")
            print("   │" + "│".join(l3) + "│")

            if row < BOARD_ROWS - 1:
                print("   ├" + "───┼" * (BOARD_COLS - 1) + "───┤")
            else:
                print("   └" + "───┴" * (BOARD_COLS - 1) + "───┘")


def load_board_from_file(filename: str = "board.json") -> Board:
    """Carga el tablero desde un archivo JSON y retorna la instancia de Board."""
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    board = Board()
    board.load_from_json(data)
    return board


if __name__ == "__main__":
    board = load_board_from_file()
    board.display()
