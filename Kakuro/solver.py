from dataclasses import dataclass
from typing import Optional


# 🧱 Base Cell Class
class Cell:
    def is_blocked(self) -> bool:
        return False

    def is_clue(self) -> bool:
        return False

    def is_empty(self) -> bool:
        return False


# ⛔ Blocked cell — does not participate
@dataclass
class BlockedCell(Cell):
    def is_blocked(self) -> bool:
        return True


# 🧮 Clue cell — contains a sum constraint for row/column
@dataclass
class ClueCell(Cell):
    right: Optional[int] = None  # Horizontal sum (right)
    down: Optional[int] = None  # Vertical sum (down)

    def is_clue(self) -> bool:
        return True


# ✏️ Empty cell — to be filled with a digit (1-9)
@dataclass
class EmptyCell(Cell):
    value: Optional[int] = None  # Value to be filled in

    def is_empty(self) -> bool:
        return True


@dataclass
class Board:
    cells: dict  # key: str like "A1", value: Cell

    def get_cell(self, coord: str) -> Cell:
        return self.cells[coord]

    def set_cell(self, coord: str, cell: Cell):
        self.cells[coord] = cell

    def display(self):
        # Encabezado
        print("     " + "   ".join(str(i) for i in range(1, 10)))
        print("   +" + "---+" * 9)

        for row in range(9):
            row_letter = chr(ord("A") + row)

            l1, l2, l3 = [f"{row_letter} |"], ["  |"], ["  |"]

            for col in range(1, 10):
                coord = f"{row_letter}{col}"
                cell = self.cells.get(coord, BlockedCell())

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

            # Imprimir 3 líneas por fila del tablero
            print(" ".join(l1) + "|")
            print(" ".join(l2) + "|")
            print(" ".join(l3) + "|")
            print("   +" + "---+" * 9)


# Creamos un tablero vacío con celdas bloqueadas
board = Board(cells={})
for row in range(9):
    for col in range(1, 10):
        coord = f"{chr(ord('A') + row)}{col}"
        board.set_cell(coord, BlockedCell())

# Añadimos algunas celdas
board.set_cell("A2", ClueCell(right=None, down=16))
board.set_cell("A3", ClueCell(right=None, down=24))
board.set_cell("B1", ClueCell(right=17, down=None))
board.set_cell("B2", EmptyCell())
board.set_cell("B3", EmptyCell())

board.set_cell("C1", ClueCell(right=29, down=None))
board.set_cell("C2", EmptyCell())
board.set_cell("C3", EmptyCell())

board.display()
