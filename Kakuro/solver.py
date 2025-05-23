from dataclasses import dataclass, field
from typing import Optional
import json


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
    cells: dict = field(default_factory=dict)

    def get_cell(self, coord: str) -> Cell:
        return self.cells[coord]

    def set_cell(self, coord: str, cell: Cell):
        self.cells[coord] = cell

    def load_from_json(self, json_data):
        for row in range(9):
            for col in range(1, 10):
                coord = f"{chr(ord('A')+row)}{col}"
                self.cells[coord] = EmptyCell()

        for coord, data in json_data.items():
            if "blockedCell" in data and data["blockedCell"] is True:
                self.cells[coord] = BlockedCell()
            elif "clueCell" in data:
                clue = data["clueCell"]
                right = clue.get("right")
                down = clue.get("down")
                self.cells[coord] = ClueCell(right=right, down=down)

    def display(self):
        # Encabezado con letras (A–I)
        letters = [chr(ord("A") + i) for i in range(9)]
        print("     " + "   ".join(letters))
        print("   +" + "---+" * 9)

        for row in range(9):
            row_letter = chr(ord("A") + row)
            row_number = f"{row + 1:>2}"

            l1, l2, l3 = [], [], []

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

            print(f"{row_number} |" + "|".join(l1) + "|")
            print("   |" + "|".join(l2) + "|")
            print("   |" + "|".join(l3) + "|")
            print("   +" + "---+" * 9)


def load_board_from_file(filename: str = "board.json") -> Board:
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    board = Board()
    board.load_from_json(data)
    return board


board = load_board_from_file()
board.display()
