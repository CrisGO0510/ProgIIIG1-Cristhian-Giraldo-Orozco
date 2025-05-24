from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Tuple, cast
import itertools
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

    def load_from_json(self, json_data):
        for row in range(9):
            for col in range(1, 10):
                coord = f"{chr(ord('A') + col - 1)}{row + 1}"
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
        print("    " + "   ".join(chr(ord("A") + i) for i in range(9)))
        print("   ┌" + "───┬" * 8 + "───┐")

        for row in range(9):
            row_number = f"{row + 1:>2}"
            l1, l2, l3 = [], [], []

            for col in range(1, 10):
                coord = f"{chr(ord('A') + col - 1)}{row + 1}"
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

            print(f"{row_number} │" + "│".join(l1) + "│")
            print("   │" + "│".join(l2) + "│")
            print("   │" + "│".join(l3) + "│")

            if row < 8:
                print("   ├" + "───┼" * 8 + "───┤")
            else:
                print("   └" + "───┴" * 8 + "───┘")

    def find_runs(self) -> Tuple[Dict[str, List[str]], Dict[str, List[str]]]:
        """
        Devuelve dos diccionarios:
        - horizontal_runs: clave = coordenada de la ClueCell con atributo right != None,
          valor = lista de coordenadas de EmptyCell a la derecha hasta el siguiente bloque.
        - vertical_runs: clave = coordenada de la ClueCell con atributo down != None,
          valor = lista de coordenadas de EmptyCell hacia abajo hasta el siguiente bloque.
        """
        horiz = {}
        vert = {}
        for coord, cell in self.cells.items():
            if isinstance(cell, ClueCell):
                row = int(coord[1:])
                col = coord[0]

                if cell.right is not None:
                    seq = []
                    c = ord(col) + 1
                    while True:
                        key = f"{chr(c)}{row}"
                        if self.get_cell(key).is_empty():
                            seq.append(key)
                            c += 1
                        else:
                            break
                    horiz[coord] = seq

                if cell.down is not None:
                    seq = []
                    r = row + 1
                    while True:
                        key = f"{col}{r}"
                        if self.get_cell(key).is_empty():
                            seq.append(key)
                            r += 1
                        else:
                            break
                    vert[coord] = seq

        return horiz, vert

    def generate_combinations(
        self, length: int, total: int | None
    ) -> List[Tuple[int, ...]]:
        """
        Devuelve todas las tuplas de longitud `length` de dígitos 1–9,
        sin repetición, que sumen `total`.
        """
        return [
            comb
            for comb in itertools.permutations(range(1, 10), length)
            if sum(comb) == total
        ]

    def solve(self) -> bool:
        """
        Solver optimizado: MRV + forward-checking incremental.
        """

        horiz_runs, vert_runs = self.find_runs()
        runs: Dict[str, List[str]] = {}
        targets: Dict[str, int] = {}

        for clue, cells in horiz_runs.items():
            runs[clue] = cells
            targets[clue] = cast(ClueCell, self.cells[clue]).right
        for clue, cells in vert_runs.items():
            runs[clue] = cells
            targets[clue] = cast(ClueCell, self.cells[clue]).down

        run_options: Dict[str, List[Tuple[int, ...]]] = {}
        for clue, cells in runs.items():
            length = len(cells)
            total = targets[clue]
            run_options[clue] = [
                comb
                for comb in itertools.permutations(range(1, 10), length)
                if sum(comb) == total
            ]

        cell_to_runs: Dict[str, List[str]] = {}
        for clue, cells in runs.items():
            for c in cells:
                cell_to_runs.setdefault(c, []).append(clue)

        unassigned: Set[str] = set(runs.keys())

        def backtrack() -> bool:
            if not unassigned:
                return True

            clue = min(unassigned, key=lambda c: len(run_options[c]))
            cells = runs[clue]

            for comb in run_options[clue]:

                ok = True
                for val, coord in zip(comb, cells):
                    existing = cast(EmptyCell, self.cells[coord]).value
                    if existing is not None and existing != val:
                        ok = False
                        break
                if not ok:
                    continue

                for val, coord in zip(comb, cells):
                    self.cells[coord].value = val

                changed: Dict[str, List[Tuple[int, ...]]] = {}
                fail = False
                for coord in cells:
                    for other in cell_to_runs[coord]:
                        if other in unassigned and other != clue:

                            if other not in changed:
                                changed[other] = run_options[other]

                                new_dom = []
                                for oc in run_options[other]:
                                    for v, cc in zip(oc, runs[other]):
                                        ev = cast(EmptyCell, self.cells[cc]).value
                                        if ev is not None and ev != v:
                                            break
                                    else:
                                        new_dom.append(oc)
                                run_options[other] = new_dom
                            if not run_options[other]:
                                fail = True
                                break
                    if fail:
                        break

                if not fail:

                    unassigned.remove(clue)
                    if backtrack():
                        return True
                    unassigned.add(clue)

                for other, old_dom in changed.items():
                    run_options[other] = old_dom
                for _, coord in zip(comb, cells):
                    self.cells[coord].value = None

            return False

        return backtrack()


def load_board_from_file(filename: str) -> Board:
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    board = Board()
    board.load_from_json(data)
    return board


if __name__ == "__main__":
    board = load_board_from_file("board.json")
    board.display()

    if board.solve():
        print("Solución encontrada:")
        board.display()
    else:
        print("No se encontró solución.")
